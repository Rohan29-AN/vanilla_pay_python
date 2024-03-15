import unittest
import hashlib
import hmac
from vanillapay.tools import extract_id_from_url,hash_data

class TestExtractIdFromUrl(unittest.TestCase):
    def test_extract_id_from_url_with_id(self):
        url="https://site_milay.com?id=123"
        id_value=extract_id_from_url(url)
        print(f"Id value: {id_value}")
        self.assertEqual(id_value,'123')

    def test_extract_id_from_url_without_id(self):
        url="https://site_milay.com/"
        id_value=extract_id_from_url(url)
        self.assertIsNone(id_value)

    def test_extract_id_with_multiple_params(self):
        url="https://site_milay.com?id=123&name=Vanilla"
        id_value=extract_id_from_url(url)
        self.assertEqual(id_value,'123')


class TestHashData(unittest.TestCase):
    def test_hash_data(self):
        secret='shutt'
        payload='vanilla pay international'

        expected_digest='2069B313561E4FE5BE48C8413E1DE1F1F983FF16D6314A6BF178AE5497A0B782'

        value=hash_data(secret,payload)

        self.assertEqual(value, expected_digest)


