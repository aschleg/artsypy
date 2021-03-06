import requests
from urllib.parse import urljoin


class Artsy(object):

    def __init__(self, key, secret=None):
        self.key = key
        self.secret = secret
        self.auth_token_uri = 'https://api.artsy.net/api/tokens/xapp_token'
        self.api_url = 'https://api.artsy.net/api'
        self.auth_token, self.token_expiry = self._get_auth_token()

    def _get_auth_token(self):
        token = requests.post(self.auth_token_uri, params={'client_id': self.key,
                                                           'client_secret': self.secret})

        token_expiry = token.json()['expires_at']
        token = token.json()['token']

        return token, token_expiry

    def get_artists(self, artist=None, artwork_id=None, similar_to_artist_id=None, similarity_type='default',
                    published_artworks=False, return_type='json'):

        endpoint_suffix = '/artists'

        if artist is None:
            endpoint = self.api_url + endpoint_suffix

        else:
            endpoint = self.api_url + endpoint_suffix + '/'
            published_artworks = None
            artist = artist.replace(' ', '-').lower()

            endpoint = urljoin(endpoint, artist)

        if similar_to_artist_id is None:
            similarity_type = None
        if not published_artworks:
            published_artworks = None
        else:
            published_artworks = str(published_artworks).lower()

        parameters = {
            'similar_to_artist_id': similar_to_artist_id,
            'similarity_type': similarity_type,
            'published': published_artworks,
            'artwork_id': artwork_id
        }

        parameters = {key: val for key, val in parameters.items() if val is not None}

        r = requests.get(endpoint,
                         headers={'X-Xapp-Token': self.auth_token},
                         params=parameters)

        if return_type == 'json':
            r = r.json()
        elif return_type == 'text':
            r = r.text
        else:
            raise ValueError("return_type parameter must be one of 'json' or 'text'.")

        return r

    def get_artworks(self, art_id=None, similar_to_artist_id=None, user_id=None):
        endpoint = self.api_url + '/artworks/'

        #if art_id is not None:
        #    endpoint = endpoint + 'artworks/' + art_id

        parameters = {
            'user_id': user_id
            #'similar_to_artwork_id': similar_to_artist_id
        }

        parameters = {key: val for key, val in parameters.items() if val is not None}

        r = requests.get(endpoint + art_id,
                         headers={'X-Xapp-Token': self.auth_token},
                         params=parameters)

        return r
