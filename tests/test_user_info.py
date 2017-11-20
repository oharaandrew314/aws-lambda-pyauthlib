'''Test UserInfo'''

import pytest

from pyauthlib import UserInfo


def test_parse_json_dict():
    '''Test parse_json from dict'''
    user1 = UserInfo.from_json(dict(
        user_id='user1',
        authorities=['authority1', 'authority2']
    ))
    assert user1.principal_id == 'user1'
    assert user1.authorities == ['authority1', 'authority2']

    user2 = UserInfo.from_json(dict(
        user_id='user2',
        authorities='authority1,authority2'
    ))
    assert user2.principal_id == 'user2'
    assert user2.authorities == ['authority1', 'authority2']


def test_parse_json_str():
    '''test parse_json from string'''
    user1 = UserInfo.from_json(
        '{ "user_id": "user1", "authorities": [ "authority1", "authority2" ] }'
    )
    assert user1.principal_id == 'user1'
    assert user1.authorities == ['authority1', 'authority2']

    user2 = UserInfo.from_json('{ "user_id": "user2", "authorities": "authority1,authority2" }')
    assert user2.principal_id == 'user2'
    assert user2.authorities == ['authority1', 'authority2']


def test_with_context():
    user = UserInfo(
        'user1', ['role1', 'role2'],
        username='User One', first_name='User', last_name='One'
    )
    assert user.principal_id == 'user1'
    assert user.as_context() == dict(
        authorities='role1,role2',
        username='User One',
        first_name='User',
        last_name='One'
    )


def test_parse_json_invalid():
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
