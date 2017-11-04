'''Test Auth Policy'''

from pyauthlib import MethodArn, AuthPolicy, UserInfo, HttpMethod


USER = UserInfo('user1', ['authority1', 'authority2'])


def test_empty_policy():
    '''Test generating an empty policy'''
    policy = AuthPolicy(USER).build()
    assert policy == dict(
        principalId=USER.user_id,
        context=dict(
            user_id='user1',
            authorities='authority1,authority2'
        ),
        policyDocument=dict(
            Version='2012-10-17',
            Statement=[]
        )
    )


def test_allow_method():
    '''Test generating a polict with one allowed method'''
    method = MethodArn('us-east-1', 'accountid', method='GET')
    policy = AuthPolicy(USER).allow(method).build()
    assert policy == dict(
        principalId=USER.user_id,
        context=dict(
            user_id='user1',
            authorities='authority1,authority2'
        ),
        policyDocument=dict(
            Version='2012-10-17',
            Statement=[
                dict(
                    Action='execute-api:Invoke',
                    Effect='Allow',
                    Resource=[str(method)]
                )
            ]
        )
    )


def test_allow_and_deny():
    '''Test policy with an allow and deny'''
    method1 = MethodArn('us-east-1', 'accountid', method='GET')
    method2 = MethodArn('us-east-1', 'accountid', method='DELETE', resource='spam/*')
    policy = AuthPolicy(USER).allow(method1).deny(method2).build()

    assert policy == dict(
        principalId=USER.user_id,
        context=dict(
            user_id='user1',
            authorities='authority1,authority2'
        ),
        policyDocument=dict(
            Version='2012-10-17',
            Statement=[
                dict(
                    Action='execute-api:Invoke',
                    Effect='Allow',
                    Resource=[str(method1)]
                ),
                dict(
                    Action='execute-api:Invoke',
                    Effect='Deny',
                    Resource=[str(method2)]
                )
            ]
        )
    )


def test_anonymous_user():
    '''Test anonymous user policy'''
    all_methods = MethodArn('us-east-1', 'accountid', HttpMethod.ALL, '*')
    policy = AuthPolicy(None).deny(all_methods).build()

    assert policy == dict(
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
                    Resource=[str(all_methods)]
                )
            ]
        )
    )
