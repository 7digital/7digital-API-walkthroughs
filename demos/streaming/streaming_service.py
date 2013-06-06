#First we define the Echonest and 7digital API keys

ECHONEST_API_KEY = "my-echonest-api-key"
SD_CONSUMER_KEY = "my-key"
SD_CONSUMER_SECRET = "my-secret"

#define the Flask application
from flask import Flask, jsonify
app = Flask(__name__)

#requests is what we use to query the echonest API
import requests

#some URL templates

ECHONEST_PLAYLIST = 'http://developer.echonest.com/api/v4/playlist/basic?api_key={key}&format=json&results=20&type=genre-radio&genre=pop&bucket=id:7digital-UK&bucket=tracks'
#Echonest helper
extract_7digital_track_id = lambda song: song["tracks"][0]["foreign_id"].split(":")[-1]

@app.route("/radio")
def get_genre_playlist():
	
	playlist_url = ECHONEST_PLAYLIST.format(key=ECHONEST_API_KEY)
	response = requests.get(playlist_url)
	
	track_ids = [extract_7digital_track_id(song) for song in response.json()["response"]["songs"]]

	return jsonify(playlist=track_ids)
	
if __name__ == "__main__" :
	app.debug = True
	app.run()
