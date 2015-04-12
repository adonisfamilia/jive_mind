from flask import Flask, request, redirect
import twilio.twiml
import spotipy
import requests
import json
import string


app = Flask(__name__)

sp = spotipy.Spotify()

@app.route('/')
def root():
    return 'Hello World!'

@app.route("/search", methods=['POST'])
def search_song():
    """Respond and greet the caller by name."""

    from_number = request.values.get('From', None)
    text_body = request.values.get('Body', None)

    text_body = string.replace(text_body, ' ', '+')
    srch_param = "https://api.spotify.com/v1/search?q=" + text_body + "&type=track"
    r = requests.get(srch_param)
    data = r.json()
    message = data['tracks']['items'][0]["id"]
    track = requests.get("https://api.spotify.com/v1/tracks/" + message)
    track_json = track.json()
    message = track_json['name'] + " " + track_json['id']

    print message
    resp = twilio.twiml.Response()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
