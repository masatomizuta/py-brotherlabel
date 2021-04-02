#!/usr/bin/env python

import brotherlabel
from PIL import Image

backend = brotherlabel.USBBackend("usb://0x04f9:0x2086")
printer = brotherlabel.PTPrinter(backend)
printer.quality = brotherlabel.Quality.high_resolution
printer.tape = brotherlabel.Tape.TZe12mm
printer.margin = 0

print(printer.get_status().to_string())

img = Image.open('label_12mm_high.png')
print(printer.print([img]).to_string())
