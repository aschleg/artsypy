import requests
from urllib.parse import urljoin


class Artsy(object):

    def __init__(self, key, secret=None):
        self.key = key
        self.secret = secret
        self.auth_token, self.token_expiry = self._get_auth_token()
        self.auth_token_uri = 'https://api.artsy.net/api/tokens/xapp_token'
        self.api_url = 'https://api.artsy.net/api'

    def _get_auth_token(self):
        token = requests.post(self.auth_token_uri, params={'client_id': self.key,
                                                           'client_secret': self.secret})

        token = token.json()['token']
        token_expiry = token.json()['expires_at']

        return token, token_expiry

    def get_artists(self, artist):
        artist_endpoint = 'https://api.artsy.net/api' + '/artists/'

        if isinstance(artist, str):
            artist = artist.replace(' ', '-').lower()

            api_call = urljoin(artist_endpoint, artist)

            r = requests.get(api_call, headers={'X-Xapp-Token': self.auth_token}).json()

        else:
            try:
                artists = list(artist)
            except TypeError:
                raise TypeError('If passing multiple artists, artist parameter must be a list or coercible into '
                                'a list.')

            r = []

            for i in range(0, len(artists)):
                artists[i] = artists[i].replace(' ', '-').lower()

                api_call = urljoin(artist_endpoint, artist)

                r.append(requests.get(api_call, headers={'X-Xapp-Token': self.auth_token}).json())

        return r
