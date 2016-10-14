blacklisted_tags = [
    '.*RADIO CITY.*',
    '.*RADIO ENERGY.*'
]
"""List of regular expressions with blacklisted tags. Blacklisted
   tags are used for detecting advertisement blocks, when the stream
   contains metadata with the song title.
   Often this title contains a fixed string during advertisement blocks,
   which makes it the ideal variant for detecting ads.
"""

max_volume = 1.0
"""Maximum volume - volume during songs"""

ad_block_volume = 0.2
"""Volume level during advertisement blocks"""
