
import requests
from core.circuit_breaker import circuit_breaker


@circuit_breaker
def shorten_url(url):
    """Shorten a URL ."""
    _VURL_URL = 'https://vurl.com/api.php?url='
    r = requests.get(_VURL_URL + url)
    return r.text
