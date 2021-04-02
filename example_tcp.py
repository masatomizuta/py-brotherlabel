#!/usr/bin/env python

import brotherlabel
from PIL import Image

backend = brotherlabel.NetworkBackend("tcp://192.168.0.10")  # Replace with your printer IP
printer = brotherlabel.PTPrinter(backend)
printer.quality = brotherlabel.Quality.high_resolution
printer.tape = brotherlabel.Tape.TZe12mm
printer.margin = 0

img = Image.open('label_12mm_high.png')
print(printer.print([img]).to_string())
