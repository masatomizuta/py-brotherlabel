#!/usr/bin/env python

# Prequisities
# 1.  Set up the printer.
# Using the P-touch Template Settings tool, specify the initial
# printer settings according to the host system environment
# or the host that the printer is connected to
#
# 2. Design the template.
# Using P-touch Editor, design the template to be transferred
# to the printer.
#
# 3. Transfer the templates.
# Using P-touch Transfer Manager, transfer the templates to
# the printer.

import brotherlabel

backend = brotherlabel.USBBackend("usb://04f9:2085")
printer = brotherlabel.PTTemplatePrinter(backend)

# NOTE: Modify template id and custom fields to correspond the template you have designed
printer.print(1, {'Object1': 'text1', 'Object2': 'text2'})