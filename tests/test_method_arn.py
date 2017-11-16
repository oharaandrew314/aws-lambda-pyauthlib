'''Test method arn parsing'''

import pytest

from pyauthlib import MethodArn, HttpMethod


def test_wildcard():
    '''Test parsing an arn with a wilcard resource'''
    arn_string = 'arn:aws:execute-api:us-east-1:1234567890:abcdefgh/latest/DELETE/*'
    arn = MethodArn.parse(arn_string)

    assert str(arn) == arn_string
    assert arn.region == 'us-east-1'
    assert arn.account_id == '1234567890'
    assert arn.rest_api_id == 'abcdefgh'
    assert arn.stage == 'latest'
    assert arn.method == HttpMethod.DELETE
    assert arn.resource == '*'


def test_nested_resource():
    '''Test parsing an ARN with a nested resource'''
    arn_string = 'arn:aws:execute-api:us-east-1:1234567890:abcdefgh/staging/GET/spam/ham/eggs'
    arn = MethodArn.parse(arn_string)

    assert str(arn) == arn_string
    assert arn.region == 'us-east-1'
    assert arn.account_id == '1234567890'
    assert arn.rest_api_id == 'abcdefgh'
    assert arn.stage == 'staging'
    assert arn.method == HttpMethod.GET
    assert arn.resource == 'spam/ham/eggs'


def test_copy():
    '''Test updating an arn'''
    arn_string = 'arn:aws:execute-api:us-east-1:1234567890:abcdefgh/latest/DELETE/foo/bar/123'
    arn = MethodArn.parse(arn_string)
    assert str(arn) == arn_string

    updated = arn.copy(method='PUT', resource='spam/ham/eggs')
    assert updated.method == HttpMethod.PUT
    assert updated.resource == 'spam/ham/eggs'
    assert str(updated) == (
        'arn:aws:execute-api:us-east-1:1234567890:abcdefgh/latest/PUT/spam/ham/eggs'
    )


def test_invalid_method():
    '''Test with an invalid http method'''
    arn_string = 'arn:aws:execute-api:us-east-1:1234567890:abcdefgh/latest/LOLCATS/foo/bar/123'
    with pytest.raises(ValueError):
        MethodArn.parse(arn_string)


def test_copy_invalid_method():
    '''Test copying with an invalid method'''
    arn_string = 'arn:aws:execute-api:us-east-1:1234567890:abcdefgh/latest/DELETE/foo/bar/123'
    arn = MethodArn.parse(arn_string)

    with pytest.raises(ValueError):
        arn.copy(method='LOLCATS')


def test_leading_resource_slash():
    '''Test with a resource that has an extra slash'''
    arn_string = 'arn:aws:execute-api:us-east-1:1234567890:abcdefgh/latest/GET//foo/bar/123'
    arn = MethodArn.parse(arn_string)
    assert arn.method == HttpMethod.GET
    assert arn.resource == 'foo/bar/123'


def test_invalid_resource():
    '''Test with an invalid resource'''
    arn_string = 'arn:aws:execute-api:us-east-1:1234567890:abcdefgh/latest/GET/foo;bar'

    with pytest.raises(ValueError):
        MethodArn.parse(arn_string)


def test_empty_resource():
    '''Test with an empty resource'''
    arn_string = 'arn:aws:execute-api:us-east-1:1234567890:abcdefgh/latest/GET/'
    method = MethodArn.parse(arn_string)
    assert method.resource == ''


def test_copy_to_root_resource():
    '''test copying to a root resource'''
    arn_string = 'arn:aws:execute-api:us-east-1:1234567890:abcdefgh/latest/GET/some/path'
    method = MethodArn.parse(arn_string)

    updated = method.copy(resource='')
    assert updated.resource == ''


def test_with_tilde():
    arn_string = 'arn:aws:execute-api:us-east-1:1234567890:abcdefgh/latest/GET/some/path~foo'
    method = MethodArn.parse(arn_string)
    assert method.resource == 'some/path~foo'
