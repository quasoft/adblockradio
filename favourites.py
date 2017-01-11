import os
import userdata


class FavouritesStorage:
    FAVOURITE_SONGS_FILE = "favourite_songs.txt"
    filename = os.path.join(userdata.get_data_dir(), FAVOURITE_SONGS_FILE)

    @classmethod
    def is_song_added(cls, title):
        if not os.path.isfile(cls.filename):
            return False

        with open(cls.filename, 'r') as f:
            return title in f.read()

    @classmethod
    def add_song(cls, title):
        if cls.is_song_added(title):
            return False

        os.makedirs(os.path.dirname(cls.filename), exist_ok=True)
        with open(cls.filename, 'a+') as f:
            f.write(title + '\n')

        return True
