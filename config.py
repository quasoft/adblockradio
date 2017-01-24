from enum import Enum


class BlockMode(Enum):
    REDUCE_VOLUME = 1
    SWITCH_STATION = 2
    REDUCE_AND_SWITCH = 3


# Sample configuration of blacklisted tags:
blacklisted_tags = [
    '.*MYRADIO123.*',        # Block anything with title containing 'MYRADIO123' text (usually name of radio)
    '^(?![\s\S])',           # Block anything that has no title
    '.*HATE THAT SONG.*',    # Block a song with specific title 'HATE THAT SONG'
]
"""List of regular expressions with blacklisted tags. Blacklisted
tags are used for detecting advertisement blocks, when the stream
contains metadata with the song title.
Often this title contains a fixed string during advertisement blocks,
which makes it the ideal variant for detecting ads.
"""

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

ad_block_volume = 0.1
"""Volume level during advertisement blocks"""

stations = [
    {'name': 'MyRadio123', 'uri': 'http://exampleofurltostream.local/stream.m3u'},
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
