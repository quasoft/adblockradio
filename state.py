import dispatchers
from storage import Storage


class StateStorage(Storage):
    filename = "last_station.txt"

    @classmethod
    def get_last_station(cls):
        return cls.read()

    @classmethod
    def set_last_station(cls, value):
        cls.overwrite(value)

dispatchers.player.change_station_clicked += lambda station: StateStorage.set_last_station(station["uri"])
