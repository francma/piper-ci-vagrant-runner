import json
import logging
import os
import uuid
from collections import defaultdict

from pathlib import Path
from typing import Optional

import pytest

from piper_vagrant.models.config import Config
from piper_vagrant.models.job import ResponseJobStatus, RequestJobStatus, Job

logging.basicConfig()
logging.getLogger('piper-vagrant').setLevel(logging.DEBUG)


@pytest.fixture(scope="session", autouse=True)
def correct_privkey_permissions(request):
    os.chmod('tests/keys/privkey_repo', 0o600)
    os.chmod('tests/keys/privkey_submodule', 0o600)


class FakeConnection:

    def __init__(self):
        self.jobs = list()
        self.statuses = defaultdict(list)
        self.logs = defaultdict(str)

    def fetch_job(self, token: str) -> Optional[Job]:
        if len(self.jobs) == 0:
            return None

        return self.jobs.pop()

    def push_job(self, job: str):
        with open('tests/jobs/{}.json'.format(job)) as fd:
            self.jobs.append(Job(json.load(fd)))

    def report(self, secret: str, status: RequestJobStatus, log: Optional[str] = None) -> ResponseJobStatus:
        self.statuses[secret].append(status)
        self.logs[secret] += '' if log is None else log

        return ResponseJobStatus.OK


@pytest.fixture()
def connection():
    conn = FakeConnection()

    return conn


@pytest.fixture()
def config():
    cfg = {
        'vagrant': {
            'vagrant_files_home': str(Path(os.path.dirname(os.path.realpath(__file__))).joinpath('vagrant-files'))
        },
        'runner': {
            'token': uuid.uuid4().hex,
            'endpoint': 'http://localhost',
        }
    }
    return Config(cfg)


@pytest.fixture()
def empty_clone(monkeypatch):
    monkeypatch.setattr('piper_vagrant.models.git.clone', lambda a, b, c, d, e=None: None)
