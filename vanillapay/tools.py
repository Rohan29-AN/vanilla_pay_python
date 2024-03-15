from urllib.parse import urlparse, parse_qs
import hashlib
import hmac

def extract_id_from_url(url):
    """
    Extracts the value of the 'id' parameter from a URL.

    Args:
        url (str): The URL from which to extract the 'id' parameter value.

    Returns:
        str: The value of the 'id' parameter if found, else None.
    """
    
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    id_value = query_params.get('id', [None])[0]

    return id_value


def hash_data(secret, payload):
    bytes_payload = payload.encode('utf-8')
    hmac_sha256 = hmac.new(secret.encode('utf-8'), bytes_payload, hashlib.sha256)
    digest = hmac_sha256.digest()
    return digest.hex().upper()
