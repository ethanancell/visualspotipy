'''
Scope is how much access Spotipy needs.
Time offset is a variable for correcting the beats relative to the song.
If the beats don't quite line up but still seem to be sort of in time, mess with that.
It defaults to 0;
'''

scope = 'user-library-modify playlist-modify-public user-top-read playlist-read-private user-read-email ' \
        'user-follow-read user-modify-playback-state user-read-currently-playing user-read-playback-state streaming ' \
        'app-remote-control '

time_offset = 0.0
