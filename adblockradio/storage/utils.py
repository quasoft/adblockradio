import os


def get_last_utf8_char(filename, ignore_newlines=True):
    """
    Reads the last character of a UTF-8 text file.
    :param filename: The path to the text file to read
    :param ignore_newlines: Set to true, if the newline character at the end of the file should be ignored
    :return: Returns the last UTF-8 character in the file or None, if the file is empty
    """
    with open(filename, 'rb') as f:
        last_char = None

        # Reads last 4 bytes, as the maximum size of an UTF-8 character is 4 bytes
        num_bytes_to_read = 4

        # If ignore_newlines is True, read two more bytes, as a newline character
        # can be up to 2 bytes (eg. \r\n)
        # and we might have a newline character at the end of file
        # or size bytes, if file's size is less than 4 bytes
        if ignore_newlines:
            num_bytes_to_read += 2

        size = os.fstat(f.fileno()).st_size
        f.seek(-min(num_bytes_to_read, size), os.SEEK_END)
        last_bytes = f.read()

        # Find the first byte of a UTF-8 character, starting
        # from the last byte
        offset = -1
        while abs(offset) <= len(last_bytes):
            b = last_bytes[offset]
            if ignore_newlines and b in b'\r\n':
                offset -= 1
                continue
            if b & 0b10000000 == 0 or b & 0b11000000 == 0b11000000:
                # If this is first byte of a UTF8 character,
                # interpret this and all bytes after it as UTF-8
                last_char = last_bytes[offset:].decode('utf-8')
                break
            offset -= 1

        if last_char and ignore_newlines:
            last_char = last_char.replace('\r', '').replace('\n', '')

        return last_char
