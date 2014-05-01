#!/usr/bin/python
# -*- coding: utf-8 -*-

from args import *
from photoSorter import *
from photoIndexer import *


class Command:
    def __init__(self, args):
        if args.index_option:
            self.indexer(args)
        else:
            self.solve(args)
        return

    @staticmethod
    def solve(args):
        PhotoSorter(args)

    @staticmethod
    def indexer(args):
        PhotoIndexer(args)


if __name__ == '__main__':
    Command(Args())
