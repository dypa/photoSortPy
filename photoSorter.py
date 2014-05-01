import re
import imghdr
from datetime import datetime

from logger import *
from fileSystem import *


class PhotoSorterException(Exception):
    logging.getLogger('app').debug('App failed')
    pass


class PhotoSorter:
    FILE_FORMAT = '%H-%M-%S_%Y-%m-%d'
    DIR_FORMAT = '/%Y/%m-%Y/%d-%m-%Y'

    VIDEO_EXTENSIONS = [
        '.avi',
        '.thm',
        '.mp4',
        '.mov',
        '.3gp',
        '.mpg',
    ]

    def __init__(self, args):
        self.fs = FileSystem()
        get_logger('app', 'logs/app.log', level=logging.DEBUG)
        logging.getLogger('app').debug('App started')

        get_logger('images', 'logs/images.log')
        get_logger('videos', 'logs/videos.log')
        get_logger('other', 'logs/other.log')

        self.scan_dir = args.scan_option
        self.storage_dir = args.storage_option
        self.fs.apply_callback_to_file_iterator(self.scan_dir, self.sorter)

        logging.getLogger('app').debug('App stoped normaly')

    def read_image_date(self, image_type, filename):
        if image_type in ('gif', 'png'):
            date_time = self.read_file_date(filename)
        elif image_type == 'jpeg':
            date_time = self.read_exif_date(filename)
        else:
            raise PhotoSorterException('Unknown image type')
        return date_time

    @staticmethod
    def read_file_date(filename):
        return datetime.fromtimestamp(os.path.getmtime(filename))

    def read_exif_date(self, filename):
        file = open(filename, 'rb')
        r = re.compile(b'\d{4}[:]\d{2}[:]\d{2}\s\d{2}[:]\d{2}[:]\d{2}', re.M)
        matches = r.search(file.read())
        if matches is None:
            datetime_original = self.read_file_date(filename)
        else:
            datetime_original = datetime.strptime(matches.group(0).decode("utf-8"), '%Y:%m:%d %H:%M:%S')
        return datetime_original

    def progress_image(self, filename, date_time, image_type):
        dirname = self.storage_dir + date_time.strftime(self.DIR_FORMAT)
        self.fs.ensure_dir_exists(dirname)
        md5 = self.fs.md5_file(filename)
        newfilename = dirname + '/' + date_time.strftime(self.FILE_FORMAT) + '.' + md5 + '.' + (
            'jpg' if image_type == 'jpeg' else image_type).upper()
        if not os.path.isfile(newfilename):
            self.fs.copy(filename, newfilename)
            logging.getLogger('images').info(md5 + ' ' + filename + ' => ' + newfilename)
        else:
            logging.getLogger('app').debug('Skip: ' + filename)
        return

    def sorter(self, filename):
        image_type = imghdr.what(filename)
        if image_type:
            self.progress_image(filename, self.read_image_date(image_type, filename), image_type)
        elif os.path.splitext(filename)[-1].lower() in self.VIDEO_EXTENSIONS:
            logging.getLogger('videos').info(self.read_file_date(filename).strftime(self.FILE_FORMAT) + ' ' + filename)
        else:
            logging.getLogger('other').info(filename)
