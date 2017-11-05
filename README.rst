aws-lambda-pyauthlib
====================

.. image:: https://img.shields.io/pypi/status/aws-lambda-pyauthlib.svg
    :target: https://pypi.org/project/aws-lambda-pyauthlib

.. image:: https://travis-ci.org/oharaandrew314/aws-lambda-pyauthlib.svg?branch=master
    :target: https://travis-ci.org/oharaandrew314/aws-lambda-pyauthlib
    
.. image:: https://img.shields.io/pypi/v/aws-lambda-pyauthlib.svg
    :target: https://pypi.org/project/aws-lambda-pyauthlib

.. image:: https://img.shields.io/pypi/l/aws-lambda-pyauthlib.svg
    :target: https://pypi.org/project/aws-lambda-pyauthlib

.. image:: https://img.shields.io/pypi/pyversions/aws-lambda-pyauthlib.svg
    :target: https://pypi.org/project/aws-lambda-pyauthlib
    
.. image:: https://codecov.io/github/oharaandrew314/aws-lambda-pyauthlib/coverage.svg?branch=master
    :target: https://codecov.io/github/oharaandrew314/aws-lambda-pyauthlib
    :alt: codecov.io

A python helper library for AWS API Gateway Custom Authorizers.

*pyauthlib* is meant to give you a set of commonly used modules to make your own AWS API Gateway Custom Authorizers.

Installation
------------

.. code-block:: bash

    pip install aws-lambda-pyauthlib

or

.. code-block:: bash

    pipenv install aws-lambda-pyauthlib


Quickstart
----------

.. code-block:: python

    '''authorizer_handler.py'''
    from pyauthlib import UserInfo, AuthPolicy, HttpMethod, parse_event
    from my_auth_client import get_client

    def lambda_handler(event, _context):
        '''Exchanges access token for user_info and returns the policy.
            Unauthorized users are denied all access.
            Users are allowed read access to all resources.
            Admins are allowed full access to all resources.
        '''
        event = parse_event(event)
    
        identity = get_client().get_identity(event.access_token)
        user_info = UserInfo(identity['user_id'], identity['grants'])
        policy = AuthPolicy(user_info)

        if not user_info:
            policy.deny(event.arn(method=HttpMethod.ALL, resource='*'))
        elif 'ROLE_ADMIN' in user_info.authorities:
            policy.allow(event.arn(method=HttpMethod.ALL, resource='*'))
        else:
            policy.allow(event.arn(method=HttpMethod.GET, resource='*'))

        return policy.build()
    
More Information
----------------

Go check out the `examples <https://github.com/oharaandrew314/aws-lambda-pyauthlib/tree/master/examples>`_!
