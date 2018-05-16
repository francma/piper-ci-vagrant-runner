from time import sleep
from io import StringIO
from typing import Optional
from datetime import timedelta
from pathlib import Path
import tempfile
import subprocess
import shutil
import os

import vagrant

from piper_vagrant.models.config import VagrantConfig
from piper_vagrant.models.job import Job
# from piper_vagrant.models.errors import PScriptException


class BufferHandler:

    def __init__(self):
        self._mem = StringIO()

    def handle_message(self, data: str) -> None:
        self._mem.write(data)

    def pop(self) -> str:
        data = self._mem.getvalue()
        self._mem.truncate(0)
        self._mem.seek(0)
        return data


class Script:

    POLL_TIMEOUT = timedelta(milliseconds=100)

    def __init__(self, job: Job, repository_path: Path, vagrant_client: vagrant.Vagrant, config: VagrantConfig) -> None:
        self._job = job
        self._repository_path = repository_path
        self._tempdir = Path(tempfile.mkdtemp())
        self._vagrant = vagrant_client
        self._vagrant_config = config

    def __enter__(self):
        vagrant_file_path = self._vagrant_config.vagrant_files_home.joinpath(self._job.image).joinpath('Vagrantfile')
        shutil.copyfile(str(vagrant_file_path), str(self._tempdir.joinpath('Vagrantfile')))
        self._vagrant.root = str(self._tempdir)
        self._vagrant.env = {**os.environ, **{'PIPER_REPOSITORY_PATH': str(self._repository_path)}}
        self._vagrant.up()

        command = self._job.script
        self._process = subprocess.Popen(
            ['vagrant', 'ssh', '--no-tty', '-c', command],
            stdout=subprocess.PIPE,
            cwd=str(self._tempdir),
            env=self._vagrant.env,
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._vagrant is not None:
            try:
                self._vagrant.halt()
            except Exception as e:
                raise e

        try:
            shutil.rmtree(str(self._tempdir))
        except Exception:
            pass  # ignore

    def poll(self, timeout: timedelta) -> str:
        while timeout > timedelta(0):
            if self._process.returncode is not None:
                break

            if timeout > self.POLL_TIMEOUT:
                sleep(self.POLL_TIMEOUT.total_seconds())
            else:
                sleep(timeout.total_seconds())

            timeout -= self.POLL_TIMEOUT
            self._process.poll()

        return self._process.stdout.read().decode('utf-8')

    @property
    def status(self) -> Optional[int]:
        return self._process.returncode
