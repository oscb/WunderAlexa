import dateutil.parser
import enum
import os
import requests
import urllib
import urlparse

import WunderPython.WunderClient


class WunderAPI(object):

    BASE_URL = 'https://a.wunderlist.com/api/v1/'

    def __init__(self, client_id, token):
        self.client_id = client_id
        self.token = token

    def get(self, endpoint, uid=None, **kwargs):
        self.__validate_token()

        if uid is not None:
            id_path = os.path.join(endpoint, uid)
            url = urlparse.urljoin(WunderAPI.BASE_URL, id_path)
        else:
            url = urlparse.urljoin(WunderAPI.BASE_URL, endpoint)

        if kwargs is not None and len(kwargs) > 0:
            url += '?{}'.format(urllib.urlencode(kwargs))

        r = requests.get(url,
                     headers=self.__get_auth_headers())
        r.raise_for_status()
        return r.json()

    def post(self, endpoint, obj):
        self.__validate_token()
        url = urlparse.urljoin(WunderAPI.BASE_URL, endpoint)
        r = requests.post(url,
                          json=obj,
                          headers=self.__get_auth_headers())
        r.raise_for_status()
        return r.json()

    def patch(self, endpoint, uid, obj):
        self.__validate_token()
        url = urlparse.urljoin(WunderAPI.BASE_URL, endpoint, uid)
        r = requests.patch(url,
                           json=obj,
                           headers=self.__get_auth_headers())
        r.raise_for_status()
        return r.json()

    def delete(self, endpoint, uid):
        self.__validate_token()
        url = urlparse.urljoin(WunderAPI.BASE_URL, endpoint, uid)
        r = requests.delete(url,
                            headers=self.__get_auth_headers())
        r.raise_for_status()
        if r.status_code is 204:
            return True
        return False

    def __validate_token(self):
        if self.token is None:
            raise Exception("Missing API Token. "
                            "Call GetToken First to get a token")

    def __get_auth_headers(self):
        headers = {
            'X-Access-Token': self.token,
            'X-Client-ID': self.client_id
        }
        return headers

###################
# Utils
###################


class SupportedTypes(enum.Enum):
    int = 1
    double = 2
    string = 3
    datetime = 4
    bool = 5


def extract_property(data, name, data_type=None, default=None):
    val = data[name] if name in data else default
    # Cast
    # DateTime
    if data_type is SupportedTypes.datetime:
        try:
            val = dateutil.parser.parse(str(val))
        except Exception:
            WunderPython.WunderClient.log.warn(
                'Error casting %s for %s as datetime',
                val, name
            )
    # TODO: Other casts if needed
    return val
