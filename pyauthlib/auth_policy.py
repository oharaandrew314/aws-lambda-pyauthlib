'''AWS Authorizer Policy'''

from pyauthlib import UserInfo


class AuthPolicy(object):
    '''AWS Authorizer Policy'''

    ANONYMOUS_USER = UserInfo('anonymous', 'ROLE_ANONYMOUS')

    VERSION = '2012-10-17'

    def __init__(self, user_info):
        self.user_info = user_info or self.ANONYMOUS_USER
        self.allow_methods = []
        self.deny_methods = []

    # def allow(self, method_arn, conditions=None):
    def allow(self, method_arn):
        '''Allow a method to be executed'''
        self.allow_methods.append(dict(
            resourceArn=str(method_arn)
            # resourceArn=str(method_arn),
            # conditions=conditions or list()
        ))
        return self

    # def deny(self, method_arn, conditions=None):
    def deny(self, method_arn):
        '''Disallow a method from being executed'''
        self.deny_methods.append(dict(
            resourceArn=str(method_arn)
            # resourceArn=str(method_arn),
            # conditions=conditions or list()
        ))
        return self

    def _get_empty_statement(self, effect):
        '''Returns an empty statement object prepopulated with the correct action and the
        desired effect.'''
        statement = {
            'Action': 'execute-api:Invoke',
            'Effect': effect[:1].upper() + effect[1:].lower(),
            'Resource': []
        }

        return statement

    def _get_statement_for_effect(self, effect, methods):
        '''This function loops over an array of objects containing a resourceArn and
        conditions statement and generates the array of statements for the policy.'''
        statements = []

        if methods:
            statement = self._get_empty_statement(effect)

            for cur_method in methods:
                # if not cur_method['conditions']:
                statement['Resource'].append(cur_method['resourceArn'])
                # else:
                #     conditional_statement = self._get_empty_statement(effect)
                #     conditional_statement['Resource'].append(cur_method['resourceArn'])
                #     conditional_statement['Condition'] = cur_method['conditions']
                #     statements.append(conditional_statement)

            if statement['Resource']:
                statements.append(statement)

        return statements

    def build(self):
        '''Generates the policy document based on the internal lists of allowed and denied
        conditions. This will generate a policy with two main statements for the effect:
        one statement for Allow and one statement for Deny.
        Methods that includes conditions will have their own statement in the policy.'''
        statements = list()
        statements.extend(self._get_statement_for_effect('Allow', self.allow_methods))
        statements.extend(self._get_statement_for_effect('Deny', self.deny_methods))

        return dict(
            principalId=self.user_info.user_id,
            context=self.user_info.to_dict(),
            policyDocument=dict(
                Version=self.VERSION,
                Statement=statements
            )
        )
