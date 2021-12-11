import os

from youtube_client import YouTubeClient
from spotify_client import SpotifyClient

# For each video in the playlist, get the song information from YouTube
def get_songs_information(youtube_client, chosen_playlist):
    songs = youtube_client.get_videos_from_playlist(chosen_playlist.id)
    return songs

#  Search for the songs on spotify.
#  If we found the song, add it to our Spotify Liked Songs.
def search_and_add_songs_to_spotify(spotify_client, songs):
     print(f"Attempting to add {len(songs)}")
     for song in songs:
        spotify_song_id = spotify_client.search_song(song.artist, song.track)
        if spotify_song_id:
            added_song = spotify_client.add_song(spotify_song_id)
            if added_song:
               print (f"Added {song.artist}")


# 1. Get the list of playlists from youtube.
# 2. Choose the playlist we what to get the videos from
# 3. Get the songs information.
# 4. Search and add the songs to spotify.
def run():
    spotyfy_token = input("Enter Spotify Token: ")
    youtube_client = YouTubeClient('./creds/client_secret.json')
    spotify_client = SpotifyClient(spotyfy_token)
    playlists = youtube_client.get_playlists()
    chosen_playlist = youtube_client.choose_playlist_from_youtube(playlists)
    songs_info = get_songs_information(youtube_client,chosen_playlist)
    search_and_add_songs_to_spotify (spotify_client, songs_info)
     

if __name__ == '__main__':
    run()


