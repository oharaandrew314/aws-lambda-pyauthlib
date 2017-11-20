'''Authorizer Example with JWT Token'''

import jwt
from jwt.exceptions import DecodeError

from pyauthlib import UserInfo, AuthPolicy, HttpMethod, parse_event

JWT_SECRET = 'secret'


def lambda_handler(event, _context):
    '''Decodes JWT token into UserInfo and returns the policy.

        Unauthorized users are denied all access.
        Users are allowed read access to all resources.
        Admins are allowed full access to all resources.
    '''
    event = parse_event(event)

    try:
        identity = jwt.decode(event.access_token, JWT_SECRET)
        user_info = UserInfo(
            identity['user_id'],
            identity['authorities'],
            fav_food=identity['fav_food']
        )
    except DecodeError:
        user_info = None

    policy = AuthPolicy(user_info)
    if not user_info:
        policy.deny(event.arn(method=HttpMethod.ALL, resource='*'))
    elif 'ROLE_ADMIN' in user_info.authorities:
        policy.allow(event.arn(method=HttpMethod.ALL, resource='*'))
    else:
        policy.allow(event.arn(method=HttpMethod.GET, resource='*'))

    return policy.build()


def test_unauthenticated():
    '''Test the policy of an unauthenticated user'''
    event = dict(
        authorizationToken='Bearer toll_troll',
        methodArn='arn:aws:execute-api:us-east-1:account_id:rest_api_id/prod/GET/'
    )

    assert lambda_handler(event, None) == dict(
        principalId='anonymous',
        context=dict(
            authorities='ROLE_ANONYMOUS'
        ),
        policyDocument=dict(
            Version='2012-10-17',
            Statement=[
                dict(
                    Action='execute-api:Invoke',
                    Effect='Deny',
                    Resource=['arn:aws:execute-api:us-east-1:account_id:rest_api_id/prod/*/*']
                )
            ]
        )
    )


def test_user():
    '''Test the policy of a read-only user'''
    jwt_token = jwt.encode(
        dict(user_id='user', authorities='ROLE_USER,ROLE_RANDOM_AUTHORITY', fav_food='cookies'),
        JWT_SECRET
    ).decode('utf-8')

    event = dict(
        authorizationToken='Bearer ' + jwt_token,
        methodArn='arn:aws:execute-api:us-east-1:account_id:rest_api_id/prod/GET/'
    )

    assert lambda_handler(event, None) == dict(
        principalId='user',
        context=dict(
            authorities='ROLE_USER,ROLE_RANDOM_AUTHORITY',
            fav_food='cookies'
        ),
        policyDocument=dict(
            Version='2012-10-17',
            Statement=[
                dict(
                    Action='execute-api:Invoke',
                    Effect='Allow',
                    Resource=['arn:aws:execute-api:us-east-1:account_id:rest_api_id/prod/GET/*']
                )
            ]
        )
    )


def test_admin():
    '''Test the policy of an admin user'''
    jwt_token = jwt.encode(
        dict(user_id='admin', authorities='ROLE_ADMIN', fav_food='Tequila'),
        JWT_SECRET
    ).decode('utf-8')

    event = dict(
        authorizationToken='Bearer ' + jwt_token,
        methodArn='arn:aws:execute-api:us-east-1:account_id:rest_api_id/prod/GET/'
    )

    assert lambda_handler(event, None) == dict(
        principalId='admin',
        context=dict(
            authorities='ROLE_ADMIN',
            fav_food='Tequila'
        ),
        policyDocument=dict(
            Version='2012-10-17',
            Statement=[
                dict(
                    Action='execute-api:Invoke',
                    Effect='Allow',
                    Resource=['arn:aws:execute-api:us-east-1:account_id:rest_api_id/prod/*/*']
                )
            ]
        )
    )
