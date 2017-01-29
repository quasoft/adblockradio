from event import Event


class AppDispatcher:
    @Event
    def exit_clicked(self):
        pass


class PlayerDispatcher:
    @Event
    def play_clicked(self):
        pass

    @Event
    def pause_clicked(self):
        pass

    @Event
    def change_station_clicked(self, station):
        pass

    @Event
    def playing_started(self):
        pass

    @Event
    def playing_paused(self):
        pass

    @Event
    def song_changed(self, title):
        pass

    @Event
    def station_changed(self, station):
        pass

    @Event
    def playing_state_changed(self, new_state):
        pass


class RecorderDispatcher:
    @Event
    def start_record_clicked(self, title):
        pass

    @Event
    def stop_record_clicked(self):
        pass

    @Event
    def recording_started(self, title):
        pass

    @Event
    def recording_stopped(self):
        pass

    @Event
    def recording_state_changed(self, new_state):
        pass


class StorageDispatcher:
    @Event
    def add_to_favourites_clicked(self, title):
        pass

    @Event
    def blacklist_song_clicked(self, title):
        pass

    @Event
    def manage_favourites_clicked(self):
        pass

    @Event
    def manage_blacklist_clicked(self):
        pass


app = AppDispatcher()
player = PlayerDispatcher()
recorder = RecorderDispatcher()
storage = StorageDispatcher()
