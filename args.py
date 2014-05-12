import os
from argparse import ArgumentParser


class ArgumentException(Exception):
    pass


class Args:
    def __init__(self):
        parser = ArgumentParser(usage="usage: %(prog)s [arguments]")
        parser.add_argument("--version", action="version", version="%(prog)s 1.0")
        parser.add_argument("--scan", help="source directory")
        parser.add_argument("--storage", help="storage directory")
        parser.add_argument("-i", "--index", action="store_true", help="index storage directory")
        self.options = parser.parse_args()

    @property
    def scan_option(self):
        if self.options.scan is not None:
            scan_dir = self.options.scan
        else:
            raise ArgumentException("no --scan= option set")

        if not os.path.isdir(scan_dir):
            raise ArgumentException("--scan= is not folder")

        return os.path.abspath(scan_dir)

    @property
    def storage_option(self):
        if self.options.storage is not None:
            storage_dir = self.options.storage
        else:
            raise ArgumentException("no --storage option set")

        if not os.path.isdir(storage_dir):
            raise ArgumentException("--storage= is not folder")

        if not os.access(scan_dir, os.W_OK):
            raise ArgumentException("--scan= is not writeable folder")

        return os.path.abspath(storage_dir)

    @property
    def index_option(self):
        return self.options.index
