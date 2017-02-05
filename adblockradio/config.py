from enum import Enum


class BlockMode(Enum):
    REDUCE_VOLUME = 1
    SWITCH_STATION = 2
    REDUCE_AND_SWITCH = 3

block_mode = BlockMode.REDUCE_AND_SWITCH
"""Choose what should happen when an advertisement block is detected:

   * BlockMode.REDUCE_VOLUME - Attenuate audio during advertisement blocks.
     This mode can cause long periods of silence (for the duration of the
     advertisement block) if min_level is set to a value close to zero.

   * BlockMode.SWITCH_STATION - Switch to another (randomly chosen) radio station.
     This mode switches to another radio station, immediately after an advertisement
     is detected. This can cause frequent switches of stations if the radio station
     often emits short ads with the station name.

   * BlockMode.REDUCE_AND_SWITCH - Initially reduces volume when ad is detected. If the
     duration of the advertisement block is longer than max_adblock_duration, switch
     to another radio station.

"""

max_ad_duration = 12
"""Maximum allowed duration of advertisement blocks in seconds.
Only used if block_mode is set to BlockMode.REDUCE_AND_SWITCH.

"""

max_volume = 1.0
"""Maximum volume - volume during songs"""

ad_block_volume = 0.02
"""Volume level during advertisement blocks"""

stations = [
    {'name': 'Energy', 'uri': 'http://stream.radioreklama.bg:80/nrj128'},   # Ice metadata tags
    {'name': 'NJoy', 'uri': 'http://46.10.150.123:80/njoy.mp3'},            # Empty tags during advertisement blocks.
    #{'name': 'Star FM', 'uri': 'http://pulsar.atlantis.bg:8000/starfm'},    # No stream tags!
    #{'name': 'Z-Rock', 'uri': 'http://46.10.150.123:80/z-rock.mp3'},        # No stream tags!
    {'name': 'Radio 1', 'uri': 'http://stream.radioreklama.bg:80/radio1128'},  # Ice metadata tags
    {'name': 'Radio 1 Rock', 'uri': 'http://stream.radioreklama.bg:80/radio1rock.ogg'},  # Tags only in ogg audio data.
    {'name': 'City', 'uri': 'http://stream.radioreklama.bg:80/city64'},     # Ice metadata tags
    #{'name': 'Energy-90s', 'uri': 'http://stream.radioreklama.bg:80/energy-90s'},  # No stream tags!
]
"""Replace these with URLs to streams of your favourite radio stations.
Currently playlists like m3u are not supported, and you need to
provider an URL to the stream itself.
"""

show_systray_tooltip = True

show_song_title = True

user_agent = 'iTunes/9.1.1'

recording = {
    'codec_name': 'lamemp3enc',
    'codec_props': {'target': 1, 'bitrate': 128, 'cbr': 1},
    'mux_name': 'id3mux',
    'mux_props': {},
    'file_ext': 'mp3',
    'create_segments': True,
    'prerecord': True
}
"""Dictionary with recording parameters:
    codec_name (str): Name of GStreamer codec plugin to use for encoding of data before writing to file
    codec_props (dict): Properties of GStreamer codec plugin
    mux_name (str): Name of GStreamer mux plugin to use as file format
    mux_props (dict): Properties of GStreamer mux plugin
    file_ext (str): File extension for recorded files (should be related to muxer)
    create_segments (bool): Specifies if a new segment should be created when creating a new file.
"""
