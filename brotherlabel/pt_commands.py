#!/usr/bin/env python
from __future__ import division
import struct
from enum import IntEnum


class CommandMode(IntEnum):
    ESC_P = 0
    Raster = 1
    Template = 3


class Commands(object):

    @staticmethod
    def invalidate():
        # type: () -> bytearray
        return b'\x00' * 200

    @staticmethod
    def initialize():
        # type: () -> bytearray
        return b'\x1B\x40'

    @staticmethod
    def status_information_request():
        # type: () -> bytearray
        return b'\x1B\x69\x53'

    @staticmethod
    def switch_dynamic_command_mode(mode):
        # type: (CommandMode) -> bytearray
        return b'\x1B\x69\x61' + bytearray([mode.value])

    @staticmethod
    def print_information_command(
            flag_quality=True,
            flag_recover=True,
            media_type=None,
            media_width=None,
            media_length=None,
            raster_number=0,
            page=0
    ):
        # type: (bool, bool, Any, Any, Any, int, int) -> bytearray
        flag = 0

        if media_type is None:
            media_type = 0
        else:
            flag |= 0x02

        if media_width is None:
            media_width = 0
        else:
            flag |= 0x04

        if media_length is None:
            media_length = 0
        else:
            flag |= 0x08

        flag |= 0x40 if flag_quality else 0
        flag |= 0x80 if flag_recover else 0

        return b'\x1B\x69\x7A' + \
               bytearray([flag, media_type, media_width, media_length]) + \
               struct.pack('<I', raster_number) + \
               bytearray([page]) + \
               b'\x00'

    @staticmethod
    def various_mode_settings(auto_cut=True, mirror=False):
        # type: (bool, bool) -> bytearray
        param = 0x40 if auto_cut else 0
        param |= 0x80 if mirror else 0
        return b'\x1B\x69\x4D' + bytearray([param])

    @staticmethod
    def specify_page_number(n=1):
        # type: (int) -> bytearray
        assert 1 <= n <= 99
        return b'\x1B\x69\x41' + bytearray([n])

    @staticmethod
    def advanced_mode_settings(draft=False, half_cut=False, no_chain=True, special_tape=False, high_resolution=False,
                               no_buffer_clear=False):
        # type: (bool, bool, bool, bool, bool, bool) -> bytearray
        param = 0x01 if draft else 0
        param |= 0x04 if half_cut else 0
        param |= 0x08 if no_chain else 0
        param |= 0x10 if special_tape else 0
        param |= 0x40 if high_resolution else 0
        param |= 0x80 if no_buffer_clear else 0
        return b'\x1B\x69\x4B' + bytearray([param])

    @staticmethod
    def specify_margin_amount(dots=0):
        # type: (int) -> bytearray
        assert dots < 65536
        return b'\x1B\x69\x64' + struct.pack('<H', dots)

    @staticmethod
    def select_compression_mode(tiff=False):
        # type: (bool) -> bytearray
        return b'\x4D' + (b'\x02' if tiff else b'\x00')

    @staticmethod
    def raster_graphics_transfer(data):
        # type: (bytearray) -> bytearray
        return b'\x47' + struct.pack('<H', len(data)) + data

    @staticmethod
    def zero_raster_graphics():
        # type: () -> bytearray
        return b'\x5A'

    @staticmethod
    def print_command():
        # type: () -> bytearray
        return b'\x0C'

    @staticmethod
    def print_command_with_feeding():
        # type: () -> bytearray
        return b'\x1A'
