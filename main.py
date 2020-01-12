'''
Username can be found by going to your settings in the desktop app.
client_id, client_secret, and redirect_uri are all made in the
Spotify Developer Dashboard. Create an app there and link it to visualspotipy.

Also, create a file called client.py in the root directory with the following variables:
username = 'YOUR_SPOTIFY_USERNAME'
client_id = 'YOUR_SPOTIFY_APP_CLIENT_ID'
client_secret = 'YOUR_SPOTIFY_APP_CLIENT_SECRET'
redirect_uri = 'http://localhost/'
'''

import sys
import time
import spotipy
import spotipy.util as util

import client
import config

# The track we will look at
analysis_id = 'spotify:track:4Sz1LV8m7zng0orrckK2OH'

# Playback requires a list for some reason
analysis_id_list = [analysis_id]

# Get user credentials
token = util.prompt_for_user_token(client.username, config.scope, client_id=client.client_id, client_secret=client.client_secret, redirect_uri=client.redirect_uri)

if not token:
    print("Can't get a valid user token for ", client.username)
    sys.exit()

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
        current_timesig = analysis_sections[current_section - 1]['time_signature']
        print("\nSection {} \t Time Signature {}").format(current_section, current_timesig)


    current_time = time.time() - start_of_song
    # Print a beat
    if beat_unplayed[current_beat] and analysis_beats[current_beat + 1]['start'] > current_time > \
            analysis_beats[current_beat]['start']:
        beat_unplayed[current_beat] = False
        current_beat += 1
        if analysis_beats[current_beat - 1]['confidence'] > 0.4:
            print("Beat {}").format(current_beat)

    # Set what the current time in the song is
    current_time = time.time() - start_of_song
