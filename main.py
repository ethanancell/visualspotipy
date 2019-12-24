import spotipy
import spotipy.util as util

import os
import time
from time import sleep

# How much access does this app have? Quite a bit apparently
scope = 'user-library-modify playlist-modify-public user-top-read playlist-read-private user-read-email ' \
        'user-follow-read user-modify-playback-state user-read-currently-playing user-read-playback-state streaming ' \
        'app-remote-control '

# Use system environment variables to get token
username = os.environ.get('SPOTIPY_CLIENT_USERNAME')
client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = 'http://localhost/'

# The track we will look at
analysis_id = 'spotify:track:2LfUYXF8jfrHCfwYyf2pRj'

# Playback requires a list for some reason
analysis_id_list = [analysis_id]

# Get user credentials
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)

    # Perform analysis
    analysis = sp.audio_analysis(analysis_id)
    analysis_sections = analysis['sections']
    analysis_bars = analysis['bars']
    analysis_beats = analysis['beats']

    # Get track information
    analysis_track = sp.track(analysis_id)

    # Start the playback
    sp.start_playback(uris=analysis_id_list)

    # Start of the song to measure how far in we are
    start_of_song = time.time()
    length_of_song = analysis_track['duration_ms'] / 1000

    # Set up the beats, sections, and bars
    beat_unplayed = [True] * len(analysis_beats)
    section_unplayed = [True] * len(analysis_sections)
    bar_unplayed = [True] * len(analysis_bars)
    current_beat = 0
    current_section = 0
    current_bar = 0

    # Loop through the song
    current_time = time.time() - start_of_song
    while current_time < length_of_song:
        current_time = time.time() - start_of_song
        # Print a section
        if section_unplayed[current_section] and analysis_sections[current_section + 1]['start'] > current_time > \
                analysis_sections[current_section]['start']:
            section_unplayed[current_section] = False
            current_section += 1
            print(
                f"\nSection {current_section} \t Time Signature {analysis_sections[current_section - 1]['time_signature']}")

        current_time = time.time() - start_of_song
        # Print a beat
        if beat_unplayed[current_beat] and analysis_beats[current_beat + 1]['start'] > current_time > \
                analysis_beats[current_beat]['start']:
            beat_unplayed[current_beat] = False
            current_beat += 1
            if analysis_beats[current_beat - 1]['confidence'] > 0.4:
                print(f"Beat {current_beat}")

        # Set what the current time in the song is
        current_time = time.time() - start_of_song

else:
    print("Can't get a valid user token for ", username)
