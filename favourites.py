from storage import Storage


class FavouritesStorage(Storage):
    filename = "favourite_songs.txt"

    @classmethod
    def is_song_added(cls, title):
        return cls.is_added(title)

    @classmethod
    def add_song(cls, title):
        if cls.is_song_added(title):
            return False

        return cls.add_line(title)
