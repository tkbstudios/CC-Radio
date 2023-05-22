import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def get_bearer():
    """Get Bearer token from spotify API"""
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": os.environ.get("SPOTIFY_API_CLIENT_ID"),
        "client_secret": os.environ.get("SPOTIFY_API_SECRET")
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        print("Error getting bearer token!")
        sys.exit(1)
    else:
        return response.json()

def search_playlists(query, bearer_token):
    """Search for uncopyrighted song playlists"""
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    params = {
        "q": query,
        "type": "playlist",
        "limit": 50  # You can set the limit to a number between 1 and 50
    }

    response = requests.get(url, headers=headers, params=params, timeout=20)
    return response.json()

def extract_playlist_urls(search_results):
    """Get playlist URLs from search results"""
    playlist_urls = []
    playlists = search_results["playlists"]["items"]

    for playlist in playlists:
        playlist_urls.append(playlist["external_urls"]["spotify"])

    return playlist_urls

def download_playlists(playlist_urls, output_dir="unconverted"):
    """Download playlist from URLs to unconverted dir"""
    playlists_count = len(playlist_urls)
    print(f"DOWNLOADING {playlists_count} playlists..")

    time.sleep(2)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for playlist_url in playlist_urls:
        try:
            os.system(f"spotdl {playlist_url} --output {output_dir}")
        except OSError:
            print(f"Error downloading {playlist_url}")
            continue

bearer_token = get_bearer()['access_token']

search_results = search_playlists("Uncopyrighted", bearer_token)

playlist_urls = extract_playlist_urls(search_results)

download_playlists(playlist_urls)
