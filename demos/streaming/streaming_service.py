# Echonest and 7digital API keys
from consumer_keys import *

# Flask application
from flask import Flask, jsonify
app = Flask(__name__)

# requests is what we use to query the echonest API
import requests

# some URL templates:
ECHONEST_PLAYLIST_URL = 'http://developer.echonest.com/api/v4/playlist/basic?api_key={key}&format=json&results=20&type=genre-radio&genre=pop&bucket=id:7digital-UK&bucket=tracks'
SD_STREAMING_URL = 'http://stream.svc.7digital.net/stream/catalogue'
SD_INFO_URL = 'http://api.7digital.com/1.2/track/details'

# set up our OAuth 1.0 signer and helper
import oauth
consumer = oauth.OAuthConsumer(SD_CONSUMER_KEY, SD_CONSUMER_SECRET)

def sign_url(url, querystring) : 
	oauth_req = oauth.OAuthRequest.from_consumer_and_token(consumer, http_url=url, parameters=querystring)
	oauth_req.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, None)
	return oauth_req.to_url()

# Echonest helper
extract_7digital_track_id = lambda song: song["tracks"][0]["foreign_id"].split(":")[-1]

# 7digital API playlist helper
make_playlist_item = lambda track_id: {
								'streaming_url': sign_url(SD_STREAMING_URL, {"trackId": track_id}),
								'info_url': sign_url(SD_INFO_URL, {"trackId": track_id})
								}

@app.route("/radio")
def get_genre_playlist() :
	
	playlist_url = ECHONEST_PLAYLIST_URL.format(key=ECHONEST_API_KEY)
	response = requests.get(playlist_url)

	if response.status_code != 200 :
		return "No echonest response received, is your ECHONEST_API_KEY set correctly?"

	track_ids = [extract_7digital_track_id(song) for song in response.json()["response"]["songs"]]

	playlist = [make_playlist_item(track_id) for track_id in track_ids]

	return jsonify(playlist=playlist)
	
if __name__ == "__main__" :
	app.debug = True
	app.run()
