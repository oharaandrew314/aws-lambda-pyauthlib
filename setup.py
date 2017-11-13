'''setup.py'''

from setuptools import setup

README_FILENAME = 'README.rst'

with open(README_FILENAME, 'r') as f:
    README = f.read()

setup(
    name='aws-lambda-pyauthlib',
    version='0.1.1',
    packages=['pyauthlib'],

    # PyPI metadata
    author='Andrew O\'Hara',
    author_email='andrew@andrewohara.io',
    description='A python helper library for AWS API Gateway Custom Authorizers',
    long_description=(README),
    license='MIT',
    url='https://github.com/oharaandrew314/aws-lambda-pyauthlib/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ]
)
