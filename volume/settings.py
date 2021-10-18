from sys import path as syspath
from os import path, environ

LOG_CLASS = 'py-scheduler'
APP_PATH = path.abspath(path.dirname(__file__))
CLI_PATH = path.abspath(path.join(APP_PATH, 'cli'))
DATA_PATH = path.abspath(path.join(APP_PATH, 'data'))

# pipenv
syspath.insert(0, APP_PATH)
activate_this = path.join(APP_PATH, '.venv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# load_env
if path.exists('.env'):
    with open('.env', encoding='UTF-8') as f:
        for _e in list(f.readlines()):
            if not _e.startswith('#') and '=' in _e:
                _k, _v = _e.strip('\n').split('=')
                environ[_k] = _v
