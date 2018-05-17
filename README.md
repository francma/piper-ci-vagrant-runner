# PIPER CI Vagrant Runner

[![Build Status](https://travis-ci.org/francma/piper-ci-vagrant-runner.svg?branch=master)](https://travis-ci.org/francma/piper-ci-lxd-runner)
[![Coverage Status](https://coveralls.io/repos/github/francma/piper-ci-vagrant-runner/badge.svg?branch=master)](https://coveralls.io/github/francma/piper-ci-vagrant-runner?branch=master)

Runner for [piper-ci-core](https://github.com/francma/piper-ci-driver) using [Vagrant](https://www.vagrantup.com/).

## Table of contents

- [Requirements](#requirements-non-pipy)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running](#running)
- [Developer guide](#developer-guide)

## Requirements (non-pipy)

- [Vagrant](https://www.vagrantup.com/)
- Python >= 3.5
- git >= 2.3.0
- ssh

## Installation

1. [Install project dependencies (non-pipy)](#requirements-non-pipy)

2. Install project from github

    `pip install git+https://github.com/francma/piper-ci-vagrant-runner.git`

## Configuration

1. Copy example configuration

    `cp config.example.yml config.yml`

2. Edit your config to fit your needs

    `vim /config.example.yml`

3. Go to `vagrant.vagrant_files_home` you defined in config and define images used in build

	`cd [vagrant.vagrant_files_home] && mkdir ubuntu && cd ubuntu && vagrant init ubuntu/trusty64` 

4. This will create Vagrantfile in `[vagrant.vagrant_files_home]/ubuntu` that will be available as `image: ubuntu` in `.piper.yml` build config file

5. In order to have repository inside your vagrant box, you must add it as synced folder to your Vagrantfile (example in `/tests/vagrant-files/ubuntu/Vagrantfile`)

	`config.vm.synced_folder ENV['PIPER_REPOSITORY_PATH'], "/piper"`

## Running

`piper-vagrant [path to your config file]`

## Developer guide

### Setup Python environment

1. Install Python virtual environment (via pip or your distribution package manager)

   `pip3 install virtualenv virtualenvwrapper`

2. Create new virtual environment named `piper-vagrant`

   `mkvirtualenv piper-vagrant`
   
3. [Install project](#installation)

4. Install dev dependencies

   `pip install -e ".[dev]"`
   
5. Deactivate virtualenv

    `deactivate`
    
6. Activate virtualenv

    `workon piper-vagrant`

### Tests

Run tests in `tests/` directory:

`pytest` or `tox -e py`

Check PEP8:

`flake8` or `tox -e pep8`

Check types:

`mypy piper_vagrant/run.py` or `tox -e mypy`

Run for specific python version:

`tox -e py35-mypy` or `tox -e py36`

Run all:

`tox`
