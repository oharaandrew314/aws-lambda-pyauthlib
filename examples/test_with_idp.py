'''Authorizer Example with mock identity provider'''

from pyauthlib import UserInfo, MethodArn, AuthPolicy, HttpMethod


class IdpClient(object):
    '''Mock external Identity provider.

        A real client would make a request to an external IDP to get the user info.
    '''

    GRANTS = dict(
        user_token=UserInfo('user', 'ROLE_USER'),
        admin_token=UserInfo('admin', 'ROLE_ADMIN')
    )

    def user_info(self, access_token):
        '''Return the user_info associated with the access token, or None'''
        if access_token not in self.GRANTS:
            return None

        return self.GRANTS[access_token]


def lambda_handler(event, _context):
    '''Exchanges access token for user_info and returns the policy.

        Unauthorized users are denied all access.
        Users are allowed read access to all resources.
        Admins are allowed full access to all resources.
    '''
    called_method = MethodArn.parse(event['methodArn'])

    _, access_token = event['authorizationToken'].split(' ')
    user_info = IdpClient().user_info(access_token)

    policy = AuthPolicy(user_info)

    if not user_info:
        policy.deny(called_method.copy(method=HttpMethod.ALL, resource='*'))
    elif 'ROLE_ADMIN' in user_info.authorities:
        policy.allow(called_method.copy(method=HttpMethod.ALL, resource='*'))
    else:
        policy.allow(called_method.copy(method=HttpMethod.GET, resource='*'))

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
            user_id='anonymous',
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
    event = dict(
        authorizationToken='Bearer user_token',
        methodArn='arn:aws:execute-api:us-east-1:account_id:rest_api_id/prod/GET/'
    )

    assert lambda_handler(event, None) == dict(
        principalId='user',
        context=dict(
            user_id='user',
            authorities='ROLE_USER'
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
    event = dict(
        authorizationToken='Bearer admin_token',
        methodArn='arn:aws:execute-api:us-east-1:account_id:rest_api_id/prod/GET/'
    )

    assert lambda_handler(event, None) == dict(
        principalId='admin',
        context=dict(
            user_id='admin',
            authorities='ROLE_ADMIN'
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
