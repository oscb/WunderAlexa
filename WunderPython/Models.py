import collections

import WunderPython
import WunderPython.API

######################################
#
# PROPERTIES
#   - name : ( default_value, type )
#
######################################
# TODO
# PropertyInfo = collections.namedtuple('PropertyInfo', ['name', 'default', 'type'])
# PropertyInfo(name='id', default=None, type=None)

class _WunderlistObject(object):
    def __init__(self, client):
        self._client = client
        self._validate_client()
        self._validate_settings()

    def save(self):
        self._validate_client()
        props = self.to_json()

        if self.id is not None:
            # Update
            obj = self._client.patch(self.ENDPOINT, self.id, props)
        else:
            # Create
            obj = self._client.post(self.ENDPOINT, props)

        #TODO: Correct?
        if obj is not None:
            self.load_from_json(**obj)

    def to_json(self):
        # Send only relevant properties
        props = {}
        for prop in self.PROPERTIES.keys():
            val = getattr(self, prop, None)
            if val is not None:
                props[prop] = val
        return props

    def load_from_json(self, **kwargs):
        for prop, propInfo in self.PROPERTIES.iteritems():
            default_val, data_type = propInfo
            val = WunderPython.API.extract_property(name=prop, data=kwargs, data_type=data_type, default=default_val)
            if getattr(self, prop, default_val) is default_val:
                setattr(self, prop, val)

    def _validate_client(self):
        if self._client is None:
            raise Exception("Missing API Client")
        if not isinstance(self._client, WunderPython.API.WunderAPI):
            raise Exception("API Client must implement APIInterface")

    def _validate_settings(self):
        if self.PROPERTIES is None:
            raise Exception("Missing PROPERTIES")

        if self.ENDPOINT is None:
            raise Exception("Missing ENDPOINT")


class List(_WunderlistObject):
    ENDPOINT = 'lists'

    PROPERTIES = {
        'id': (None, None),
        'created_at': (None, WunderPython.API.SupportedTypes.datetime),
        'title': (None, None),
        'list_type': (None, None),
        'revision': (None, None)
    }

    def __init__(self,
                 client=None,
                 **kwargs
                 ):
        super(List, self).__init__(client)
        self.tasks = []

        if len(kwargs) > 0:
            self.load_from_json(**kwargs)

    def get_tasks(self):
        self._validate_client()
        tasks = self._client.get(Task.ENDPOINT, list_id=self.id)
        self.tasks = [Task(client=self._client, list=self, **t) for t in tasks]
        return self.tasks

    def create_task(self, title, creation_date=None, starred=None):
        self._validate_client()
        t = Task(client=self._client,
                 list=self,
                 title=title,
                 creation_date=creation_date,
                 starred=starred)
        return t


class Task(_WunderlistObject):
    ENDPOINT = 'tasks'

    PROPERTIES = {
        'id': (None, None),
        'created_at': (None, WunderPython.API.SupportedTypes.datetime),
        'due_date': (None, WunderPython.API.SupportedTypes.datetime),
        'title': (None, None),
        'starred': (None, None),
        'revision': (None, None),
        'list_id': (None, None)
    }

    def __init__(self,
                 client=None,
                 list=None,
                 **kwargs
                 ):
        super(Task, self).__init__(client)
        self.list = list

        if len(kwargs) > 0:
            self.load_from_json(**kwargs)

    def to_json(self):
        props = super(Task, self).to_json()
        props['list_id'] = self.list.id
        return props





