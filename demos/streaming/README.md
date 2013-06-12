7digital Streaming Walkthrough
==============================

In this walkthrough we will build a simple in-browser radio-style streaming service.

We are going to use the Echonest API to generate a genre playlist, and then use the 7digital API to play that in the browser.

The server side playlist component is implemented in Python, using the Flask and Requests library. It simply returns a JSON list of 7digital URLs that have been pre-signed with your consumer key. This is so that you do not need to expose your API consumer secret to the end user.

The client side component reads this playlist and streams the audio using the HTML5 audio object, as well as displaying the cover image and track details.

Caveats
-------

This walkthrough is intended to be as simple as possible, and as such the following caveats apply - these are things that you will need to address if are building a "proper" radio-style streaming service

* The track stream is not DMCA compliant
* The track stream is different for each connected user
* There's no user or play logging
* There isn't any error handling
* Many more rough edges

How it works
============

Getting set up
--------------

First you need to register for a 7digital API key and an Echonest API key. The key and secrets for these should go into the consumer_keys.py file. To use the streaming endpoints, you need to arrange access to them with 7digital (they aren't included in the free 7digital API). Alternatively, you could use 7digital preview clips by changing the SD_STREAMING_URL in streaming_service.py to the track/preview url.

Server side component
---------------------

The purpose of this is to deliver pre-signed streaming links to the browser. We could sign links to the 7digital Streaming API directly in the browser with Javascript, but this would require us to expose the 7digital consumer secret available in the browser.

First of all we ask Echonest for a radio playlist of our chosen genre (as provided in the URL : http://127.0.0.1:5000/genre/chicago%20house

	ECHONEST_PLAYLIST_URL = 'http://developer.echonest.com/api/v4/playlist/basic?api_key={key}&format=json&results=20&type=genre-radio&genre={genre}&bucket=id:7digital-UK&bucket=tracks'

We can ask Echonest to return 7digital IDs by using the bucket=id:7digital-UK parameter. Other 7digital buckets for other territories are available, consult the Echonest documentation for more info.

The response from echonest looks like:
```json
 {
   "response": {
     "status": {
       "version": "4.2",
       "code": 0,
       "message": "Success"
     },
     "songs": [
       {
          "tracks": [
           {
             "release_image": "http://cdn.7static.com/static/img/sleeveart/00/002/747/0000274783_200.jpg",
             "foreign_release_id": "7digital-UK:release:274783",
             "preview_url": "http://previews.7digital.com/clips/34/3052623.clip.mp3",
             "catalog": "7digital-UK",
             "foreign_id": "7digital-UK:track:3052623",
             "id": "TRMDLRT12E4F0E7C11"
           },
		   ... more tracks ...
         ],
          "artist_id": "ARV3PRJ1187B99E42D",
          "id": "SOWPTKC12A81C22C0B",
          "artist_name": "Fingers Inc.",
          "title": "Never No More Lonely"
       },
	   ... more songs ...

     ]
     }
  }
 ```

We extract the 7digital track ID from the foreign_id, and use this to construct a playlist with pairs of OAuth signed links, one to the streaming API and one to the track/details endpoint:

```json
{
  "playlist": [
    {
      "info_url": "http://api.7digital.com/1.2/track/details?oauth_version=1.0&oauth_signature=qdXgyVQUSXnq1nDY4yj6vxdgM40%3D&imageSize=350&oauth_nonce=36860626&oauth_timestamp=1371047874&trackId=14259160&oauth_consumer_key=my_key&oauth_signature_method=HMAC-SHA1",
      "streaming_url": "http://stream.svc.7digital.net/stream/catalogue?oauth_nonce=68593495&oauth_timestamp=1371047874&trackId=14259160&oauth_consumer_key=my_key&oauth_signature_method=HMAC-SHA1&oauth_version=1.0&oauth_signature=AApuNrKBRoI6xAX8nfkUMvjAYjI%3D"
    },
... more links ...
}
```

Client side component
---------------------

We use jQuery to request a playlist for the genre we've selected. This is passed to the playTrack function which loads the streaming_url into an HTML5 audio object, and sets event listeners to download the track information once the track starts playing, and to move to the next playlist item once the current one has finished:

```js
var playTrack = function(playlistResponse, position) {
	var currentSong = playlistResponse.playlist[position];
	var player = document.getElementById("player");
	var loadTrackInfo = function() {
		player.removeEventListener("playing", loadTrackInfo);
		$.get(currentSong.info_url, displayTrackInfo);
	};

	var playNext = function() {
		player.removeEventListener("ended", playNext);
		playTrack(playlistResponse, position + 1);
	};

	player.addEventListener("ended", playNext);
	player.addEventListener("playing", loadTrackInfo);
	player.setAttribute("src", currentSong.streaming_url);
	player.pause();
	player.load();
	player.play();
};
```
