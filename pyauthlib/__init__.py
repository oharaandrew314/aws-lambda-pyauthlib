'''pyauthlib'''

from .user_info import UserInfo # noqa F401
from .method_arn import MethodArn # noqa F401
from .auth_policy import AuthPolicy # noqa F401
from .http_method import HttpMethod # noqa F401
from .auth_event import AuthEvent


def parse_event(event):
    '''Parse the Authorizer event'''
    return AuthEvent.parse(event)
