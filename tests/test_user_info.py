'''Test UserInfo'''

import pytest

from pyauthlib import UserInfo


def test_parse_json_dict():
    '''Test parse_json from dict'''
    user1 = UserInfo.from_json(dict(
        user_id='user1',
        authorities=['authority1', 'authority2']
    ))
    assert user1.user_id == 'user1'
    assert user1.authorities == ['authority1', 'authority2']

    user2 = UserInfo.from_json(dict(
        user_id='user2',
        authorities='authority1,authority2'
    ))
    assert user2.user_id == 'user2'
    assert user2.authorities == ['authority1', 'authority2']


def test_parse_json_str():
    '''test parse_json from string'''
    user1 = UserInfo.from_json(
        '{ "user_id": "user1", "authorities": [ "authority1", "authority2" ] }'
    )
    assert user1.user_id == 'user1'
    assert user1.authorities == ['authority1', 'authority2']

    user2 = UserInfo.from_json('{ "user_id": "user2", "authorities": "authority1,authority2" }')
    assert user2.user_id == 'user2'
    assert user2.authorities == ['authority1', 'authority2']


def test_parse_json_invalidy():
    '''Test parsing various forms of invalid input'''
    with pytest.raises(ValueError):
        UserInfo.from_json('')

    with pytest.raises(KeyError):
        UserInfo.from_json(dict())

    with pytest.raises(KeyError):
        UserInfo.from_json(dict(user_id='user1'))

    with pytest.raises(KeyError):
        UserInfo.from_json(dict(authorities='authority1'))

    with pytest.raises(ValueError):
        UserInfo.from_json('lol')


def test_invalid_authorities():
    '''Test where authorities is invalid'''
    with pytest.raises(ValueError):
        UserInfo.from_json(dict(
            user_id='user_id',
            authorities=1337
        ))
