import pytest
import vcr
import os
from artsypy.api import Artsy


tape = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    serializer='json',
    record_mode='once'
)


key = os.environ.get('ARTSY_KEY')
secret = os.environ.get('ARTSY_SECRET')


def authenticate():
    artsy = Artsy(str(key), str(secret))

    return artsy


artsy = authenticate()


def test_get_auth_token():
    assert isinstance(artsy.auth_token, str)
    assert isinstance(artsy.token_expiry, str)


@vcr.use_cassette('tests/cassettes/get_artists.yml', filter_query_parameters=['key', 'secret'])
def test_get_artists():
    artist = 'Andy Warhol'

    r_json = artsy.get_artists(artist)

    assert isinstance(r_json['_links'], dict)

    r_str = artsy.get_artists(artist, return_type='text')

    assert isinstance(r_str, str)
    assert r_str[1:32] == '"id":"4d8b92b34eb68a1b2c0003f4"'

    r_similar = artsy.get_artists(similar_to_artist_id='4d8b92b34eb68a1b2c0003f4')

    assert isinstance(r_similar['_embedded']['artists'], list)

    r_artwork = artsy.get_artists(artwork_id='516dfb9ab31e2b2270000c45')

    assert r_artwork['_embedded']['artists'][0]['name'] == 'William Michael Harnett'

    with pytest.raises(ValueError):
        artsy.get_artists(artist, return_type='sjsfgerf')
