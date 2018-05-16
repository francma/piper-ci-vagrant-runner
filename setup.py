from setuptools import setup, find_packages

long_description = ""

setup(
    name='piper_vagrant',
    version='0.01',
    description='Piper CI Vagrant Runner',
    long_description=long_description,
    packages=find_packages(),
    package_dir={'piper_vagrant': 'piper_vagrant'},
    author='Martin Franc',
    author_email='francma6@fit.cvut.cz',
    keywords='vagrant,ci,runner,piper',
    url='https://github.com/francma/piper-ci-vagrant-runner',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
          'piper-vagrant = piper_vagrant.run:main'
        ]
    },
    install_requires=[
        # requests to piper-core
        'requests',
        # Vagrant
        'python-vagrant',
        # yaml config file
        'pyyaml',
        # JSON schema validation
        'pykwalify',
    ],
    extras_require={
        'dev': [
            # type checking
            'mypy',
            'tox',
            'coveralls',
            'pytest>=3',
            'pytest-timeout',
            'pytest-cov',
        ],
    },
)
