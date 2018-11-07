#!/usr/bin/env python

import struct
from enum import IntEnum


class CommandMode(IntEnum):
    ESC_P = 0
    Raster = 1
    Template = 3


class Commands(object):

    @staticmethod
    def invalidate() -> bytes:
        return b'\x00' * 200

    @staticmethod
    def initialize() -> bytes:
        return b'\x1B\x40'

    @staticmethod
    def status_information_request() -> bytes:
        return b'\x1B\x69\x53'

    @staticmethod
    def switch_dynamic_command_mode(mode: CommandMode) -> bytes:
        return b'\x1B\x69\x61' + bytes([mode.value])

    @staticmethod
    def print_information_command(
            flag_quality=True,
            flag_recover=True,
            media_type=None,
            media_width=None,
            media_length=None,
            raster_number=0,
            page=0
    ) -> bytes:
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
               bytes([flag, media_type, media_width, media_length]) + \
               struct.pack('<I', raster_number) + \
               bytes([page]) + \
               b'\x00'

    @staticmethod
    def various_mode_settings(auto_cut=True, mirror=False) -> bytes:
        param = 0x40 if auto_cut else 0
        param |= 0x80 if mirror else 0
        return b'\x1B\x69\x4D' + bytes([param])

    @staticmethod
    def specify_page_number(n=1) -> bytes:
        assert 1 <= n <= 99
        return b'\x1B\x69\x41' + bytes([n])

    @staticmethod
    def advanced_mode_settings(draft=False, half_cut=False, no_chain=True, special_tape=False, high_resolution=False,
                               no_buffer_clear=False) -> bytes:
        param = 0x01 if draft else 0
        param |= 0x04 if half_cut else 0
        param |= 0x08 if no_chain else 0
        param |= 0x10 if special_tape else 0
        param |= 0x40 if high_resolution else 0
        param |= 0x80 if no_buffer_clear else 0
        return b'\x1B\x69\x4B' + bytes([param])

    @staticmethod
    def specify_margin_amount(dots=0) -> bytes:
        assert dots < 65536
        return b'\x1B\x69\x64' + struct.pack('<H', dots)

    @staticmethod
    def select_compression_mode(tiff=False) -> bytes:
        return b'\x4D' + (b'\x02' if tiff else b'\x00')

    @staticmethod
    def raster_graphics_transfer(data: bytes) -> bytes:
        return b'\x47' + struct.pack('<H', len(data)) + data

    @staticmethod
    def zero_raster_graphics() -> bytes:
        return b'\x5A'

    @staticmethod
    def print_command() -> bytes:
        return b'\x0C'

    @staticmethod
    def print_command_with_feeding() -> bytes:
        return b'\x1A'
