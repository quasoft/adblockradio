import os
import userdata


class Storage:
    filename = "last_station.txt"

    @classmethod
    def get_filepath(cls):
        return os.path.join(userdata.get_data_dir(), cls.filename)

    @classmethod
    def file_exists(cls):
        return os.path.isfile(cls.get_filepath())

    @classmethod
    def makedirs(cls):
        os.makedirs(os.path.dirname(cls.get_filepath()), exist_ok=True)

    @classmethod
    def open(cls, mode):
        if any(c in mode for c in 'aw+'):
            cls.makedirs()
        return open(cls.get_filepath(), mode)

    @classmethod
    def read(cls):
        if not cls.file_exists():
            return ""

        with cls.open('r') as f:
            return f.read()

    @classmethod
    def overwrite(cls, text):
        with cls.open('a+') as f:
            f.truncate(0)
            f.write(text)

    @classmethod
    def is_added(cls, text):
        if not cls.file_exists():
            return False

        with cls.open('r') as f:
            return text in f.read()

    @classmethod
    def add_line(cls, text):
        with cls.open('a+') as f:
            f.write(text + '\n')

        return True
