import requests
import logging
import urlparse
import WunderPython

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)

def create_client(client_id, client_secret):
    return WunderClient(client_id, client_secret)


class WunderClient:

    def __init__(self, client_id, client_secret):
        self.client_ID = client_id
        self.client_secret = client_secret
        self.token = None
        self.api = None

    def authorize(self, url, state):
        base_url = "https://www.wunderlist.com/oauth/authorize?"

        params = {
            'client_id'     : self.client_ID,
            'redirect_uri'  : url,
            'state'         : state
        }
        return base_url + urlparse.urlencode(params)

    def get_token(self, code):
        base_url = "https://www.wunderlist.com/oauth/access_token"

        params = {
            'client_id'     : self.client_ID,
            'client_secret' : self.client_secret,
            'code'          : code
        }
        response = requests.post(base_url, data=params)
        json_resp = response.json()
        self.token = json_resp['access_token']
        return self.token

    def build(self):
        self.api = WunderPython.API.WunderAPI(self.client_ID, self.token)

    def build(self, token):
        self.token = token
        self.api = WunderPython.API.WunderAPI(self.client_ID, self.token)

    # Lists
    def get_lists(self):
        jlists = self.api.get(WunderPython.Models.List.ENDPOINT)
        lists = [WunderPython.Models.List(client=self.api, **i) for i in jlists]
        return lists





