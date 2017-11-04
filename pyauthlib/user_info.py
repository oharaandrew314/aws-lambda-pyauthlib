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

    def __init__(self, user_id, authorities):
        if isinstance(authorities, string_types):
            authorities = authorities.split(',')
        elif not isinstance(authorities, (list, tuple)):
            raise ValueError('Authorites must be comma-seperated, or a list')

        self.user_id = user_id
        self.authorities = authorities

    def to_dict(self):
        '''Return the authorizer context as a dict'''
        return dict(
            user_id=self.user_id,
            authorities=','.join(self.authorities)
        )
