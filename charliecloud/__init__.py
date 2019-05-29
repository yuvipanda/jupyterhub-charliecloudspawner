"""
Python 'bindings' for charliecloud.

Should not use any scripts that depend on docker
"""
from traitlets import Unicode
from traitlets.config import LoggingConfigurable
import sys
import os
import importlib

# FIXME: Ideally this would be a *Spawner* subclass
# But JupyterHub's __init__subclass__ doesn't let you inherit from Spawner
# without implementing a bunch of methods
class CharliecloudSpawnerMixin(LoggingConfigurable):
    container_image_path = Unicode(
        'github.com--yuvipanda-example-requirements:1df775c0265c50d953c6e9078b710d4e8fbe1efa.tar.gz',
        config=True,
    )

    container_run_path = Unicode(
        '/var/tmp/{username}',
        config=True,
    )

    start_timeout = 5 * 60

    def start(self):
        expanded_container_path = self.container_run_path.format(
            username=self.user.name
        )
        self.cmd = [
            sys.executable, '-m', 'charliecloud.singleuser',
            os.path.abspath(self.container_image_path), expanded_container_path,
            '--',
        ] + self.cmd
        
        return super().start()

def mixin_spawner(spawner_class):
    if type(spawner_class) is type:
        spawner_class_type = spawner_class
    elif type(spawner_class) is str:
        spawner_class_parts = spawner_class.rsplit('.', 1)
        module = importlib.import_module(spawner_class_parts[0])
        spawner_class_type = getattr(module, spawner_class_parts[1])
    else:
        raise TypeError(
            'spawner_class should be of type str or a Class. Got {} instead'.format(
                type(spawner_class)
            ))

    class CharliecloudMixedSpawner(CharliecloudSpawnerMixin, spawner_class_type):
        pass
    return CharliecloudMixedSpawner