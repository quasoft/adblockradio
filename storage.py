import os
import userdata


class Storage:
    filename = ""

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

    @classmethod
    def read_items(cls):
        """Read all items in a list of strings
        :rtype: list of strings
        :return:
        """
        return cls.read().splitlines(keepends=False)

    @classmethod
    def write_items(cls, items):
        """Save list items to file. This overwrites the existing file.
        If the file does not exists, it is automatically created.
        :param items: list of strings
        """
        text = "\n".join(items)
        cls.overwrite(text)
