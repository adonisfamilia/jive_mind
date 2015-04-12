from flask import Flask, request, redirect, render_template
from flask_oauthlib.client import OAuth, OAuthException
import twilio.twiml
import spotipy
import spotipy.util as util
import requests
import json
import string
import pprint
import sys



app = Flask(__name__)
oauth = OAuth(app)

spotify = oauth.remote_app(
    'spotify',
    consumer_key=SPOTIFY_APP_ID,
    consumer_secret=SPOTIFY_APP_SECRET,
    # Change the scope to match whatever it us you need
    # list of scopes can be found in the url below
    # https://developer.spotify.com/web-api/using-scopes/
    request_token_params={'scope': 'user-read-email'},
    base_url='https://accounts.spotify.com',
    request_token_url=None,
    access_token_url='/api/token',
    authorize_url='https://accounts.spotify.com/authorize'
)


@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    callback = url_for(
        'spotify_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return spotify.authorize(callback=callback)

@app.route('/login/authorized')
def spotify_authorized():
    resp = spotify.authorized_response()
    if resp is None:
        return 'Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: {0}'.format(resp.message)

    session['oauth_token'] = (resp['access_token'], '')
    me = spotify.get('/me')
    return 'Logged in as id={0} name={1} redirect={2}'.format(
        me.data['id'],
        me.data['name'],
        request.args.get('next')
    )


@spotify.tokengetter
def get_spotify_oauth_token():
    return session.get('oauth_token')


@app.route("/search", methods=['POST'])
def search_song():

    from_number = request.values.get('From', None)
    text_body = request.values.get('Body', None)

    text_body = string.replace(text_body, ' ', '+')
    srch_param = "https://api.spotify.com/v1/search?q=" + text_body + "&type=track"
    r = requests.get(srch_param)
    data = r.json()
    message = data['tracks']['items'][0]["id"]
    track = requests.get("https://api.spotify.com/v1/tracks/" + message)
    track_json = track.json()
    message = track_json['name'] + " " + track_json['id'] + "-" + track_json['artist']

    print message
    resp = twilio.twiml.Response()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
