'''Test Auth Event parser'''

import pytest

from pyauthlib import parse_event, raise_401


def test_invalid_access_token():
    '''Test parsing event with invalid access token'''
    with pytest.raises(Exception) as ex_info:
        parse_event(dict(
            methodArn='arn:aws:execute-api:us-east-1:account_id:"rest_api_id/test/GET/',
            authorizationToken='foobar'
        ))

    assert str(ex_info.value) == 'Unauthorized'


def test_parse_event():
    '''Test parsing valid event'''
    event = parse_event(dict(
        methodArn='arn:aws:execute-api:us-east-1:account_id:rest_api_id/test/GET/',
        authorizationToken='Bearer foobar'
    ))

    assert event.method_arn.rest_api_id == 'rest_api_id'
    assert str(event.arn('POST', 'foo')) == (
        'arn:aws:execute-api:us-east-1:account_id:rest_api_id/test/POST/foo'
    )

    assert event.token_type == 'Bearer'
    assert event.access_token == 'foobar'


def test_401():
    with pytest.raises(Exception) as context:
        raise_401()

    assert str(context.value) == 'Unauthorized'
