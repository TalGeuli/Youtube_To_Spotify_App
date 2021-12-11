import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import youtube_dl


class Playlist(object):
    def __init__(self, _id, _title):
        self.id = _id
        self.title = _title


class Song(object):
    def __init__(self, _artist, _track):
        self.artist = _artist
        self.track = _track


class YouTubeClient(object):
    def __init__(self, credentials_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"


        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_location, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        self.youtube_client = youtube_client

    # goal: return a list of playlists that we would like to convert to a spotify playlists
    def get_playlists(self):
        request = self.youtube_client.playlists().list(
            part="id, snippet",  # what data we what from each playlist
            maxResults=50,  # maximum of 50 playlists
            mine=True  # make our own playlist
        )
        response = request.execute()

        # creat a list of playlists
        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]

        return playlists

    # goal: to extract the videos from the playlist
    def get_videos_from_playlist(self, playlist_id):
        songs = []
        request = self.youtube_client.playlistItems().list(
            playlistId=playlist_id,
            part="id,snippet"
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            artist, track = self.get_artist_and_track_from_video(video_id)
            if artist and track:
                songs.append(Song(artist,track))

        return songs

    # goal: to extract the artist and track from the video so we could use them later to find the same video in spotify
    def get_artist_and_track_from_video(self, video_id):
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(
            youtube_url, download=False
        )

        artist = video['artist']
        track = video['track']

        return artist, track

    # Ask witch playlist we want to get music videos from
    def choose_playlist_from_youtube (self, playlists):
        for index, playlist in enumerate(playlists):
            print(f"{index}: {playlist.title}")
        choice = int(input("Enter your choice: "))
        chosen_playlist = playlists[choice]
        print(f"You selected: {chosen_playlist.title}")
        return chosen_playlist


