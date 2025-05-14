#!/usr/bin/env python

import time
from enum import Enum
from logging import getLogger

from PIL import Image

from .backends import Backend
from .pt_commands import *
from .pt_status import *

_logger = getLogger(__file__)


class Tape(Enum):
    TZe3_5mm = {'print_area': 48, 'right_margin': 264}
    TZe6mm = {'print_area': 64, 'right_margin': 256}
    TZe9mm = {'print_area': 106, 'right_margin': 235}
    TZe12mm = {'print_area': 150, 'right_margin': 213}
    TZe18mm = {'print_area': 234, 'right_margin': 171}
    TZe24mm = {'print_area': 320, 'right_margin': 128}
    TZe36mm = {'print_area': 454, 'right_margin': 61}

    @property
    def print_area(self) -> int:
        return self.value['print_area']

    @property
    def right_margin(self) -> int:
        return self.value['right_margin']


class Quality(Enum):
    """ Print Quality """
    standard = 0
    """ Standard 360 x 360 dpi """
    draft = 1
    """ Draft 360 x 180 dpi """
    high_quality = 2
    """ High Quality Slow Speed 360 x 360 dpi """
    high_resolution = 3
    """ High Resolution 360 x 720 dpi """


class PTPrinter(object):
    __total_pins = 560

    def __init__(self, backend: Backend):
        self.backend = backend
        self.print_timeout_sec = 10
        self.margin = 0
        self.tape = Tape.TZe12mm
        self.quality = Quality.standard
        self.auto_cut = False
        self.half_cut = True
        self.no_chain = False
        self.special_tape = False

    def get_status(self) -> Status:
        data = Commands.invalidate()
        data += Commands.initialize()
        data += Commands.status_information_request()

        start = time.time()
        _logger.info('Sending data to the printer. Total: %d bytes.', len(data))
        self.backend.write(data)

        status = None

        while time.time() - start < 10:
            data = self.backend.read()
            if not data:
                time.sleep(0.005)
                continue

            status = Status.from_bytes(data)
            break

        return status

    @staticmethod
    def __get_raster_line(img, img_bytes, line_len: int, x: int, y_offset: int) -> bytes:
        """
        Scan a line from the image
        :return: bytes of a raster line
        """
        line = b''
        for line_idx in range(line_len):
            bits = 0
            for bit_idx in range(8):
                y = line_idx * 8 + bit_idx - y_offset
                if x < img.width and 0 <= y < img.height:
                    color = img_bytes[(x, y)]
                    if isinstance(color, int):  # grayscale
                        px = color
                    else:  # RGB
                        px = sum(color) / 3
                    bits |= (0 if px > 230 else 1) << (7 - bit_idx)
            line += struct.pack('!B', bits)
        return line

    @staticmethod
    def __get_image_bytes(img):
        if img.mode == 'P':
            img = img.convert('RGBA')

        if img.mode == 'RGBA':
            # Thanks to https://stackoverflow.com/a/9459208/35070
            new_img = Image.new('RGB', img.size, (255, 255, 255))
            new_img.paste(img, mask=img.split()[3])
            img = new_img

        return img.load()

    def print(self, images: [Image]) -> Status:
        data = Commands.invalidate()
        data += Commands.initialize()
        data += Commands.switch_dynamic_command_mode(CommandMode.Raster)
        data += Commands.various_mode_settings(auto_cut=self.auto_cut)
        data += Commands.specify_page_number(1)
        data += Commands.advanced_mode_settings(
            half_cut=self.half_cut,
            high_resolution=self.quality == Quality.high_resolution,
            draft=self.quality == Quality.draft,
            no_chain=self.no_chain,
            special_tape=self.special_tape)
        data += Commands.specify_margin_amount(self.margin)

        for i, img in enumerate(images):
            if i > 0:
                data += Commands.print_command()

            if len(images) == 1 or len(images) - 1 == i:
                page = 2
            elif i == 0:
                page = 0
            else:
                page = 1

            data += Commands.print_information_command(
                raster_number=img.width,
                page=page,
                flag_quality=self.quality in [Quality.high_quality, Quality.high_resolution])

            data += Commands.select_compression_mode(tiff=False)

            img_bytes = self.__get_image_bytes(img)
            line_len = self.__total_pins // 8
            offset = self.tape.right_margin

            for x in range(img.width):
                line = self.__get_raster_line(img, img_bytes, line_len, x, offset)
                data += Commands.raster_graphics_transfer(line)

        data += Commands.print_command_with_feeding()

        _logger.info('Sending data to the printer. Total: %d bytes.', len(data))
        self.backend.write(data)

        status = None
        start = time.time()
        while time.time() - start < self.print_timeout_sec:
            rsp = self.backend.read()
            if not rsp:
                time.sleep(0.1)
                continue

            status = Status.from_bytes(rsp)
            break

        if status is None:
            raise TimeoutError("Status did not received")

        return status

class PTTemplatePrinter(object):
    def __init__(self, backend: Backend):
        self.backend = backend

    def print(self, id, custom_fields):
        data = Commands.initialize_dynamic_settings()
        data += Commands.initialize_template_data()
        data += Commands.choose_template(id)
        assert type(custom_fields) is dict
        for key in custom_fields.keys():
            data += Commands.select_object(key)
            data += Commands.directly_insert_object(custom_fields[key])
        data += Commands.template_print()
        self.backend.write(data)