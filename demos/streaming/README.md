7digital Streaming Walkthrough
==============================

In this walkthrough we will build a simple in-browser radio-style streaming service.

We are going to use the Echonest API to generate a genre playlist, and then use the 7digital API to play that in the browser.

The server side playlist component is implemented in Python, using the Flask and Requests library. It simply returns a JSON list of 7digital URLs that have been pre-signed with your consumer key. This is so that you do not need to expose your API consumer secret to the end user.

The client side component reads this playlist and streams the audio, accompanied by track information.


