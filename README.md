# py-brotherlabel

py-brotherlabel is a Python package to control Brother P-Touch label printers in raster printing mode.
Intended to use on a Raspberry Pi board.

## Compatible Printers

- PT-P900
- PT-P900W
- PT-P950NW

## Usage

1. Connect the printer to the Raspberry Pi via USB cable and turn on the pritner.

2. Run command `lsusb`. The device ID will be listed along with the company name **Brother**.
  ```
  Bus 001 Device 004: ID 04f9:2086 Brother Industries, Ltd
  ```

3. See `example_usb.py`. Pass the device ID to `USBBackend` constructor.

## USB Device Permission

When pyusb shows the error `usb.core.USBError: [Errno 13] Access denied (insufficient permissions)`,
see https://www.raspberrypi.org/forums/viewtopic.php?t=186839

### 1. Create Rule

Example rule `/etc/udev/rules.d/50-usb-perms.rules` for PT-P900/P900W/P950NW:
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="04f9", ATTRS{idProduct}=="2083", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="04f9", ATTRS{idProduct}=="2085", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="04f9", ATTRS{idProduct}=="2086", GROUP="plugdev", MODE="0666"
```

### 2. Reload Rule

```
sudo udevadm control --reload; sudo udevadm trigger
```

## Reference

- Software Developer's Manual Raster Command Reference PT-P900/P900W/P950NW
  - [English](https://download.brother.com/welcome/docp100407/cv_ptp900_eng_raster_101.pdf)
  - [Japanese](https://download.brother.com/welcome/docp100407/cv_ptp900_jpn_raster_101.pdf)
