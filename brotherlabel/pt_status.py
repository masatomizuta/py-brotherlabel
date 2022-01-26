#!/usr/bin/env python
from __future__ import division
import ctypes
from enum import IntEnum


class ModelCode(IntEnum):
    PT_P900 = 0x71
    PT_P900W = 0x69
    PT_P950NW = 0x70


class MediaWidth(IntEnum):
    NoTape = 0x00
    W3_5mm = 0x04
    W6mm = 0x06
    W9mm = 0x09
    W12mm = 0x0C
    W18mm = 0x12
    W24mm = 0x18
    W36mm = 0x24
    FLe21mmX45mm = 0x15


class MediaType(IntEnum):
    NoMedia = 0x00
    LaminatedTape = 0x01
    NonLaminatedTape = 0x03
    FabricTape = 0x04
    HeatShrinkTube = 0x11
    FleTape = 0x13
    FlexibleIDTape = 0x14
    SatinTape = 0x15
    IncompatibleTape = 0xFF


class StatusType(IntEnum):
    ReplyToStatusRequest = 0x00
    PrintingCompleted = 0x01
    ErrorOccurred = 0x02
    ExitIFMode = 0x03
    TurnedOff = 0x04
    Notification = 0x05
    PhaseChange = 0x06


class TapeColor(IntEnum):
    White = 0x01
    Other = 0x02
    Clear = 0x03
    Red = 0x04
    Blue = 0x05
    Yellow = 0x06
    Green = 0x07
    Black = 0x08
    Clear_WhiteText = 0x09
    MatteWhite = 0x20
    MatteClear = 0x21
    MatteSilver = 0x22
    SatinGold = 0x23
    SatinSilver = 0x24
    Blue_D = 0x30
    Red_D = 0x31
    FluorescentOrange = 0x40
    FluorescentYellow = 0x41
    BerryPink_S = 0x50
    LightGray_S = 0x51
    LimeGreen_S = 0x52
    Yellow_F = 0x60
    Pink_F = 0x61
    Blue_F = 0x62
    White_HeatShrinkTube = 0x70
    White_FlexID = 0x90
    Yellow_FlexID = 0x91
    Cleaning = 0xF0
    Stencil = 0xF1
    Incompatible = 0xFF


class TextColor(IntEnum):
    White = 0x01
    Other = 0x02
    Red = 0x04
    Blue = 0x05
    Black = 0x08
    Gold = 0x0A
    Blue_F = 0x62
    Cleaning = 0xF0
    Stencil = 0xF1
    Incompatible = 0xFF


class Status(ctypes.Structure):
    _pack_ = 1

    _fields_ = [('print_head_mark', ctypes.c_ubyte),
                ('size', ctypes.c_ubyte),
                ('brother_code', ctypes.c_ubyte),
                ('series_code', ctypes.c_ubyte),
                ('model_code', ctypes.c_ubyte),
                ('country_code', ctypes.c_ubyte),
                ('battery_level', ctypes.c_ubyte),
                ('extended_error', ctypes.c_ubyte),
                ('error_info_1', ctypes.c_ubyte),
                ('error_info_2', ctypes.c_ubyte),
                ('media_width', ctypes.c_ubyte),
                ('media_type', ctypes.c_ubyte),
                ('number_of_colors', ctypes.c_ubyte),
                ('fonts', ctypes.c_ubyte),
                ('japanese_fonts', ctypes.c_ubyte),
                ('mode', ctypes.c_ubyte),
                ('density', ctypes.c_ubyte),
                ('media_length', ctypes.c_ubyte),
                ('status_type', ctypes.c_ubyte),
                ('phase_type', ctypes.c_ubyte),
                ('phase_number_high', ctypes.c_ubyte),
                ('phase_number_low', ctypes.c_ubyte),
                ('notification_number', ctypes.c_ubyte),
                ('expansion_area', ctypes.c_ubyte),
                ('tape_color', ctypes.c_ubyte),
                ('text_color', ctypes.c_ubyte),
                ('reserved1', ctypes.c_ubyte),
                ('reserved2', ctypes.c_ubyte),
                ('reserved3', ctypes.c_ubyte),
                ('reserved4', ctypes.c_ubyte),
                ('reserved5', ctypes.c_ubyte),
                ('reserved6', ctypes.c_ubyte)]

    def to_string(self):
        # type: () -> str
        s = ""
        for field in self._fields_:
            s += '{}: 0x{:02x}\n'.format(field[0], getattr(self, field[0]))
        return s

    @classmethod
    def from_bytes(cls, data):
        # type: (bytearray) -> Self@Status
        r = cls()
        ctypes.memmove(ctypes.addressof(r), data, 32)
        return r

    def __init__(self, *args, **kwargs):
        super(Status, self).__init__(*args, **kwargs)

        self.print_head_mark = 0
        self.size = 0
        self.brother_code = 0
        self.series_code = 0
        self.model_code = 0  # type: ModelCode
        self.country_code = 0
        self.battery_level = 0
        self.extended_error = 0
        self.error_info_1 = 0
        self.error_info_2 = 0
        self.media_width = 0  # type: MediaWidth
        self.media_type = 0  # type: MediaType
        self.number_of_colors = 0
        self.fonts = 0
        self.japanese_fonts = 0
        self.mode = 0
        self.density = 0
        self.media_length = 0
        self.status_type = 0  # type: StatusType
        self.phase_type = 0
        self.phase_number_high = 0
        self.phase_number_low = 0
        self.notification_number = 0
        self.expansion_area = 0
        self.tape_color = 0  # type: TapeColor
        self.text_color = 0  # type: TextColor
        self.reserved1 = 0
        self.reserved2 = 0
        self.reserved3 = 0
        self.reserved4 = 0
        self.reserved5 = 0
        self.reserved6 = 0
