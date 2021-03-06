#!/usr/bin/env python

from abc import ABCMeta, abstractmethod


class Backend(object, metaclass=ABCMeta):
    """
    Brother printer abstract backend
    """

    @abstractmethod
    def write(self, data: bytes):
        raise NotImplementedError()

    @abstractmethod
    def read(self, length: int = 32):
        raise NotImplementedError()

    @abstractmethod
    def dispose(self):
        raise NotImplementedError()

    def __del__(self):
        try:
            self.dispose()
        except:
            pass
