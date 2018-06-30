import pytest
import vcr
from artsypy.api import Artsy


tape = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    serializer='json',
    record_mode='once'
)
