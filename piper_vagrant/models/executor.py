import logging
import multiprocessing
from datetime import timedelta
from functools import wraps
import tempfile
from pathlib import Path

import vagrant

from piper_vagrant.models.script import Script
from piper_vagrant.models.connection import Connection
from piper_vagrant.models.config import VagrantConfig
from piper_vagrant.models import git
from piper_vagrant.models.job import Job, RequestJobStatus, ResponseJobStatus
from piper_vagrant.models.errors import PStopException, PConnectionException, PScriptException


LOG = logging.getLogger('piper-vagrant')


def _catch(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        self = args[0]
        try:
            func(*args, **kwargs)
        except PConnectionException as e:
            LOG.error(str(e))
        except PScriptException as e:
            self._report_status(self._job.secret, RequestJobStatus.ERROR)
            LOG.error(str(e))
        except PStopException:
            LOG.debug('Received status != ResponseJobStatus.OK from PiperCore, stopping container')

    return wrapped


class Executor(multiprocessing.Process):

    def __init__(self, connection: Connection, interval: timedelta, vagrant_config: VagrantConfig, job: Job,
                 **kwargs) -> None:
        self._client = vagrant.Vagrant(quiet_stderr=False, quiet_stdout=False)
        self._vagrant_config = vagrant_config
        self._job = job
        self._interval = interval
        self._connection = connection
        super().__init__(**kwargs)

    @_catch
    def run(self) -> None:
        self._report_status(RequestJobStatus.RUNNING)

        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            git.clone(self._job.origin, self._job.branch, self._job.commit, path)

            with Script(self._job, path, self._client, self._vagrant_config) as script:
                while script.status is None:  # running
                    output = script.poll(self._interval)
                    self._report_status(RequestJobStatus.RUNNING, output)
                output = script.poll(self._interval)

                self._report_status(RequestJobStatus.COMPLETED, output)

    def _report_status(self, status: RequestJobStatus, data=None) -> ResponseJobStatus:
        response = self._connection.report(self._job.secret, status, data)
        if response is not ResponseJobStatus.OK:
            raise PStopException

        return response
