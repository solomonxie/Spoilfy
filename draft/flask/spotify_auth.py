import json

import requests
from authlib.client import OAuth2Session

from flask import Flask
from flask import request
from flask import redirect

# Get auth info
with open('./.client_secret.json', 'r') as f:
    data = json.loads( f.read() )
    client_id = data['client_id']
    client_secret = data['client_secret']
    scope = data['scope']
    redirect_uri = data['redirect_uri']
    authorize_url = data['authorize_url']
    access_token_url = data['access_token_url']

# Create Session
session = OAuth2Session(
    client_id, client_secret,
    scope=scope, redirect_uri=redirect_uri
)
# Generate auth url for requests
uri, state = session.create_authorization_url( authorize_url )


# Create FLask app
app = Flask(__name__)

@app.route('/')
def root():
    return 'Hello!!!!'


@app.route('/spotify/auth')
def authenticate():
    return redirect(uri)


@app.route('/spotify/callback')
def callback():
    code = request.args.get('code')
    url = request.url
    # Fetch Tokens (in dict format)
    tokens = session.fetch_access_token(
        access_token_url, authorization_response=url
    )
    print( '[Tokens]:', tokens )

    # return '[URL]:{}'.format(url)
    return redirect('/spotify/show-token?token={}'.format(tokens['access_token']))


@app.route('/spotify/show-token')
def show_token():
    return '[ACCESS TOKEN]:{}'.format(request.args.get('token'))


def main():
    app.run(host='127.0.0.1', port=80)
    

if __name__ == '__main__':
    main()
