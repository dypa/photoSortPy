import logging

from logger import get_logger
from fileSystem import FileSystem


class PhotoIndexer:
    def __init__(self, args):
        self.fs = FileSystem()
        get_logger('app', 'logs/app.log', level=logging.DEBUG)

        self.storage_dir = args.storage_option

        logging.getLogger('app').debug('App started')

        self.fs.apply_callback_to_file_iterator(self.storage_dir, self.indexer)

        logging.getLogger('app').debug('App stoped normaly')

    def indexer(self, filename):
        self.fs.check_md5(filename)
