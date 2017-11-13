'''Auth Event'''

from traceback import print_exc

from pyauthlib import MethodArn


class AuthEvent(object):
    ''''Auth Event'''

    @classmethod
    def parse(cls, event):
        '''Parse the AWS-provided authorization event.  Raises ValueError'''
        try:
            token_type, access_token = event['authorizationToken'].split(' ')
        except ValueError:
            print_exc()
            raise Exception('Unauthorized')

        return cls(
            token_type,
            access_token,
            MethodArn.parse(event['methodArn'])
        )

    def __init__(self, token_type, access_token, method_arn):
        self.token_type = token_type
        self.access_token = access_token
        self.method_arn = method_arn

    def arn(self, method=None, resource=None):
        '''Return a MethodArn for this API with the given method and resource'''
        return self.method_arn.copy(method, resource)
