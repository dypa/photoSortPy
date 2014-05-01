from logger import *
from fileSystem import *


class PhotoIndexer:
    def __init__(self, args):
        self.fs = FileSystem()
        get_logger('app', 'logs/app.log', level=logging.DEBUG)
        logging.getLogger('app').debug('App started')

        self.storage_dir = args.storage_option
        self.fs.apply_callback_to_file_iterator(self.storage_dir, self.indexer)

        logging.getLogger('app').debug('App stoped normaly')

    def indexer(self, filename):
        self.fs.check_md5(filename)
