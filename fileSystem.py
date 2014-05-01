import os
import hashlib
import errno
import shutil
import logging


class FileSystem:
    @staticmethod
    def md5_file(filename):
        md5 = hashlib.md5()
        try:
            with open(filename, 'rb') as f:
                for chunk in iter(lambda: f.read(md5.block_size), b''):
                    md5.update(chunk)
        except IOError:
            logging.getLogger('app').debug('Md5 file ' + filename + ' failed')
            raise
        return md5.hexdigest()

    @staticmethod
    def ensure_dir_exists(dirname):
        try:
            os.makedirs(dirname)
            logging.getLogger('app').debug('Make dir: ' + dirname)
        except OSError as e:
            if e.errno != errno.EEXIST:
                logging.getLogger('app').debug('Could not create dir: ' + dirname)
                raise
        return

    @staticmethod
    def apply_callback_to_file_iterator(scan_dir, func):
        for (root, subFolders, files) in os.walk(scan_dir):
            for file in files:
                func(os.path.abspath(os.path.join(root, file)))

    @staticmethod
    def copy(filename, newfilename):
        #used copy2 to save file make time
        shutil.copy2(filename, newfilename)

    def check_md5(self, filename):
        (path, name) = os.path.split(filename)
        name = name.split(".")
        if len(name) == 3 and len(name[1]) == 32:
            if self.md5_file(filename) != name[1]:
                logging.getLogger('app').critical('Wrong md5 for file: ' + filename)
        else:
            logging.getLogger('app').debug('No md5 for filename: ' + filename)
