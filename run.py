from flask import Flask, request, redirect
import twilio.twiml
import spotipy
import requests
import json


app = Flask(__name__)

sp = spotipy.Spotify()


# Try adding your own number to this list!
callers = {

}

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""

    from_number = request.values.get('From', None)
    text_body = request.values.get('Body', None)


    if from_number in callers:
        message = callers[from_number] + ", thanks for the message!"
    else:
        text_body = string.replace(text_body, ' ', '+')
        srch_param = "https://api.spotify.com/v1/search?q=" + text_body + "&type=track"
        r = requests.get("https://api.spotify.com/v1/search?q=&type=track")
        data = r.json()
        message = data['tracks']['items'][0]["id"]
        track = requests.get("https://api.spotify.com/v1/tracks/" + message)
        track_json = track.json()
        message = track_json['name']


    resp = twilio.twiml.Response()
    resp.message(text_body)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
