'''AWS API Gateway Method Arn'''

import re


from .http_method import HttpMethod


class MethodArn(object):
    '''Parses useful information from the Method ARN'''

    PATH_REGEX = re.compile(r'^[/.a-zA-Z0-9-\*]+$')

    @classmethod
    def parse(cls, method_arn):
        '''Parse a method ARN from the string'''
        _, _, _, region, account_id, api_gateway_parts = method_arn.split(':')
        rest_api_id, stage, method, resource = api_gateway_parts.split('/', 3)

        return cls(region, account_id, rest_api_id, stage, method, resource)

    @classmethod
    def _validate_method(cls, method):
        '''Validate and return the HttpMethod'''
        method = method or HttpMethod.ALL
        if not isinstance(method, HttpMethod):
            method = HttpMethod(method)

        return method

    @classmethod
    def _validate_resource(cls, resource):
        '''Validate and return the resource path'''
        resource = resource or ''
        if resource and not cls.PATH_REGEX.match(resource):
            raise ValueError('Invalid resource path: <' + resource + '>')
        elif resource[:1] == '/':  # strip leading '/'
            return resource[1:]
        return resource

    def __init__(
            self, region, account_id, rest_api_id='*', stage='*',
            method=None, resource=None
    ):
        self.account_id = account_id
        self.rest_api_id = rest_api_id
        self.region = region
        self.stage = stage
        self.method = self._validate_method(method)
        self.resource = self._validate_resource(resource)

    def copy(self, method=None, resource=None):
        '''Make a copy with a new method and/or resource'''
        return MethodArn(
            self.region, self.account_id,
            self.rest_api_id, self.stage,
            self._validate_method(method),
            self._validate_resource(resource)
        )

    def __repr__(self):
        return (
            "arn:aws:execute-api:{region}:{account_id}:"
            "{rest_api_id}/{stage}/{method}/{resource}".format(
                region=self.region,
                account_id=self.account_id,
                rest_api_id=self.rest_api_id,
                stage=self.stage,
                method=self.method.value,
                resource=self.resource
            )
        )
