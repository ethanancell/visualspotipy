# VisualSpotipy

## Getting started
To use this project, create an app in your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/login)

Get the client_id and client_secret and put them into a file called client.py in your root directory. Go to your Spotify
account and go to your settings to find your username. Create a redirect URI for your Spotify app as well, this can just be
```http://localhost/```. Put the redirect URI and username into the client file as well.

It should look like this:

```python
client_id = YOUR_CLIENT_ID
client_secret = YOUR_CLIENT_SECRET
username = YOUR_USERNAME
redirect_uri = http://localhost
```
