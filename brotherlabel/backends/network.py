#!/usr/bin/env python

"""
Backend to support Brother label printers via network.
Works cross-platform.
"""

import socket

from .backend import Backend


class NetworkBackend(Backend):
    """
    Brother backend using TCP socket
    """

    def __init__(self, device_specifier: str):
        """
        device_specifier: string: identifier in the format tcp://192.168.1.10
        """
        self.read_timeout_sec = 1
        self.write_timeout_sec = 10

        if device_specifier.startswith('tcp://'):
            device_specifier = device_specifier[6:]
        host, _, port = device_specifier.partition(':')
        if port:
            port = int(port)
        else:
            port = 9100

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.connect((host, port))
        self.socket.settimeout(self.read_timeout_sec)

    def write(self, data: bytes):
        self.socket.settimeout(self.write_timeout_sec)
        self.socket.sendall(data)
        self.socket.settimeout(self.read_timeout_sec)

    def read(self, length: int = 32) -> bytes:
        try:
            data = self.socket.recv(length)
            return data
        except socket.timeout:
            pass
        return b''

    def dispose(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
