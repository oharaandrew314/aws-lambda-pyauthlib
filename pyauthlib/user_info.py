'''User Info'''

import json

from six import string_types


class UserInfo(object):
    '''User Info'''

    @classmethod
    def from_json(cls, json_data):
        '''Parse User-Info from json'''
        if isinstance(json_data, string_types):
            json_data = json.loads(json_data)

        return cls(json_data['user_id'], json_data['authorities'])

    def __init__(self, principal_id, authorities, **extra_context):
        if isinstance(authorities, string_types):
            authorities = authorities.split(',')
        elif not isinstance(authorities, (list, tuple)):
            raise ValueError('Authorites must be comma-seperated, or a list')

        self.principal_id = principal_id
        self.authorities = authorities
        self.extra_context = extra_context

    def as_context(self):
        '''Return the authorizer context as a dict'''
        return dict(
            authorities=','.join(self.authorities),
            **self.extra_context
        )
