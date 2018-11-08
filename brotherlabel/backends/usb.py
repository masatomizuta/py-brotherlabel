#!/usr/bin/env python

"""
Backend to support Brother label printers via USB.
Works on Mac OS X and Linux.
"""

import time

import usb.core
import usb.util

from .backend import Backend


def list_available_devices():
    """
    List all available devices for the respective backend

    returns: devices: a list of dictionaries with the keys 'identifier' and 'instance': \
        [ {'identifier': 'usb://0x04f9:0x2015/C5Z315686', 'instance': pyusb.core.Device()}, ]
        The 'identifier' is of the format idVendor:idProduct_iSerialNumber.
    """

    class find_class(object):
        def __init__(self, class_):
            self._class = class_

        def __call__(self, device):
            # first, let's check the device
            if device.bDeviceClass == self._class:
                return True
            # ok, transverse all devices to find an interface that matches our class
            for cfg in device:
                # find_descriptor: what's it?
                intf = usb.util.find_descriptor(cfg, bInterfaceClass=self._class)
                if intf is not None:
                    return True
            return False

    # only Brother printers
    printers = usb.core.find(find_all=1, custom_match=find_class(7), idVendor=0x04f9)

    def identifier(dev) -> str:
        try:
            serial = usb.util.get_string(dev, 0x03)[3:]
            return 'usb://0x{:04x}:0x{:04x}_{}'.format(dev.idVendor, dev.idProduct, serial)
        except:
            return 'usb://0x{:04x}:0x{:04x}'.format(dev.idVendor, dev.idProduct)

    return [{'identifier': identifier(printer), 'instance': printer} for printer in printers]


class USBBackend(Backend):
    """
    Brother printer backend using USB
    """

    def __init__(self, device_specifier: str):
        """
        device_specifier: string: identifier in the format usb://idVendor:idProduct/iSerialNumber
        """
        self.dev = None  # type: usb.core.Device
        self.read_timeout_sec = 1
        self.write_timeout_sec = 15

        if device_specifier.startswith('usb://'):
            device_specifier = device_specifier[6:]
        vendor_product, _, serial = device_specifier.partition('/')
        vendor, _, product = vendor_product.partition(':')
        vendor, product = int(vendor, 16), int(product, 16)

        for result in list_available_devices():
            printer = result['instance']
            if printer.idVendor == vendor and printer.idProduct == product or (
                    serial and printer.iSerialNumber == serial):
                self.dev = printer
                break

        if self.dev is None:
            raise ValueError('Device not found')

        try:
            assert self.dev.is_kernel_driver_active(0)
            self.dev.detach_kernel_driver(0)
            self.was_kernel_driver_active = True
        except (NotImplementedError, AssertionError):
            self.was_kernel_driver_active = False

        # set the active configuration. With no arguments, the first configuration will be the active one
        self.dev.set_configuration()

        cfg = self.dev.get_active_configuration()
        intf = usb.util.find_descriptor(cfg, bInterfaceClass=7)
        assert intf is not None

        ep_match_in = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        ep_match_out = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT

        ep_in = usb.util.find_descriptor(intf, custom_match=ep_match_in)
        ep_out = usb.util.find_descriptor(intf, custom_match=ep_match_out)

        assert ep_in is not None
        assert ep_out is not None

        self.write_dev = ep_out  # type: usb.core.Endpoint
        self.read_dev = ep_in  # type: usb.core.Endpoint

    def _raw_read(self, length) -> bytes:
        return bytes(self.read_dev.read(length))

    def read(self, length: int = 32) -> bytes:
        data = self._raw_read(length)
        if data:
            return data

        time.sleep(self.read_timeout_sec)
        return self._raw_read(length)

    def write(self, data: bytes):
        self.write_dev.write(data, int(self.write_timeout_sec * 1000))

    def dispose(self):
        usb.util.dispose_resources(self.dev)
        del self.write_dev, self.read_dev
        if self.was_kernel_driver_active:
            self.dev.attach_kernel_driver(0)
        del self.dev
