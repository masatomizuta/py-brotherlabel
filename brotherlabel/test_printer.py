#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from brotherlabel import *


class TestPTPrinter(unittest.TestCase):

    def test_get_status(self):
        mock_backend = unittest.mock.create_autospec(spec=Backend)
        mock_backend.read.return_value = bytes(32)

        def write_handler(data: bytes):
            self.assertTrue(data.startswith(Commands.invalidate()))
            self.assertTrue(data.endswith(Commands.status_information_request()))

        mock_backend.write.side_effect = write_handler

        printer = PTPrinter(mock_backend)
        status = printer.get_status()

        mock_backend.write.assert_called_once()

        self.assertEqual(status.print_head_mark, 0)

    def test_print_single_image(self):
        mock_backend = unittest.mock.create_autospec(spec=Backend)
        mock_backend.read.return_value = bytes(32)

        def write_handler(data: bytes):
            self.assertTrue(data.startswith(Commands.invalidate()))
            self.assertTrue(data.endswith(Commands.print_command_with_feeding()))

        mock_backend.write.side_effect = write_handler

        printer = PTPrinter(mock_backend)

        img = Image.open('../label_12mm.png')

        status = printer.print([img])

        mock_backend.write.assert_called_once()

        self.assertEqual(status.print_head_mark, 0)
