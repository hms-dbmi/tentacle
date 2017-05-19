import os
from setuptools import setup

# variables used in buildout
here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
except:
    pass  # don't know why this fails with tox

requires = [
]

tests_require = [
    'pytest>=3.0.1',
    'pytest-mock',
    'pytest-cov',
]

setup(
    name='Tentacle - repo tracker',
    version=open("tentacle/_version.py").readlines()[-1].split()[-1].strip("\"'"),
    description='Tentacle - the tool for collecting repo information',
    packages=['tentacle'],
    zip_safe=False,
    author='Tech Core, DBMI',
    author_email='jeremy_johnson@hms.harvard.edu',
    url='http://techcore.dbmi.hms.harvard.edu',
    license='MIT',
    classifiers=[
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            ],
    install_requires=requires,
    include_package_data=True,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    setup_requires=['pytest-runner', ],
)
