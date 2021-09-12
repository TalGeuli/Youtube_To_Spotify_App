import os

from youtube_client import YouTubeClient
from spotify_client import SpotifyClient

def run():
    # 1. Get a list of our playlists from youtube
    youtube_client = YouTubeClient('./creds/client_secret.json')
    spotify_client = SpotifyClient('BQBBgH2qIv30RN3lDgvLoxtmXcff9AFtVUuc5peoIJ-HBiZJ3iS7AQj9IHVlIyetzjo4K-gi-erKh4Yksrfinsy3R6QkO0DzxTMar62J_APN2iz-9a81CXo7-XFRwrduF7wUOSL33fAAE4aA6s4EhEjGhDKw0aUBaygx5qXe1QW7')
    playlists = youtube_client.get_playlists()

    # 2. Ask witch playlist we want to get music videos from
    for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")
    choice = int(input("Enter your choice: "))
    chosen_playlist = playlists[choice]
    print(f"You selected: {chosen_playlist.title}")

    # 3. For each video in the playlist, get the song information from YouTube
    songs = youtube_client.get_videos_from_playlist(chosen_playlist.id)
    print(f"Attempting to add {len(songs)}")

    # 4. Search for the songs on spotify
    for song in songs:
        spotify_song_id = spotify_client.search_song(song.artist, song.track)
        if spotify_song_id:
            added_song = spotify_client.add_song(spotify_song_id)
            if added_song:
               print (f"Added {song.artist}")

    # 5. If we found the song, add it to our Spotify Liked Songs

if __name__ == '__main__':
    run()


