from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import requests

date = input("What date to you want your playlist to be based on?: ")
infoRequest = requests.get("https://www.billboard.com/charts/hot-100/" + date)
bs = BeautifulSoup(infoRequest.text, 'html.parser')
topSongs = bs.find_all(name="div", class_="o-chart-results-list-row-container")

songs = []
for song in topSongs:
    songList = song.find(name="h3", id="title-of-a-story").getText().strip()
    songs.append(songList)

spot = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="Enter your own ID",
        client_secret="Enter your own Secret",
        cache_path="Insert your account token"
    )
)

userID = spot.current_user()["id"]

songURI = []
year = date.split("-")[0]
for song in songs:
    result = spot.search(q=f"track:{song} year:{year}", type="track")
    try:
        infoURI = result["tracks"]["items"][0]["uri"]
        songURI.append(infoURI)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. It hasn't been added.")

createPlaylist = spot.user_playlist_create(user=userID, name=f"{date} Billboard 100", public=False)
spot.playlist_add_items(playlist_id=createPlaylist["id"], items=songURI)