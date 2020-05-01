from urllib.parse import urlparse, parse_qsl, urlencode
from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC

from config import APP_SECRET

class Vk:
    def __init__(self):
        pass

    def is_valid(self, query: str):
        """Check VK Apps signature"""
        params = dict(parse_qsl(urlparse(query).path, keep_blank_values=True))

        vk_subset = OrderedDict(sorted(x for x in params.items() if x[0][:3] == b"vk_"))
        
        hash_code = b64encode(HMAC(APP_SECRET.encode(), urlencode(vk_subset, doseq=True).encode(), sha256).digest())
        decoded_hash_code = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')

        return params[b"sign"].decode('utf-8') == decoded_hash_code
