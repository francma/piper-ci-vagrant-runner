from pathlib import Path
from typing import Dict, Any
from datetime import timedelta
import collections
import os

from pykwalify.core import Core as Validator

import piper_vagrant.schemas as schemas


class VagrantConfig:

    def __init__(self, vagrant_files_home: Path) -> None:
        self.vagrant_files_home = vagrant_files_home


class RunnerConfig:

    def __init__(self, token: str, interval: timedelta, instances: int, endpoint: str) -> None:
        self.token = token
        self.interval = interval
        self.instances = instances
        self.endpoint = endpoint


class LoggingConfig:

    def __init__(self, config: Dict[Any, Any]) -> None:
        self.config = config


class Config:

    _DEFAULTS = {
        'vagrant': {
            'vagrant_files_home': os.path.expanduser('~/.piper-vagrant/vagrant-files'),
        },
        'runner': {
            'interval': 3,
            'instances': 1,
            'repository_dir': '/tmp',
        },
        'logging': {
            'version': 1,
        },
    }

    def __init__(self, d: Dict[Any, Any]) -> None:
        validator = Validator(schema_data=schemas.config, source_data=d)
        validator.validate()
        config = self._merge_dicts(self._DEFAULTS, d)

        self.logging = LoggingConfig(config['logging'])
        self.vagrant = VagrantConfig(
            Path(config['vagrant']['vagrant_files_home']),
        )
        self.runner = RunnerConfig(
            token=config['runner']['token'],
            interval=timedelta(seconds=config['runner']['interval']),
            instances=config['runner']['instances'],
            endpoint=config['runner']['endpoint'],
        )

    def _merge_dicts(self, d, u):
        for k, v in u.items():
            if isinstance(v, collections.Mapping):
                r = self._merge_dicts(d.get(k, {}), v)
                d[k] = r
            else:
                d[k] = u[k]
        return d
