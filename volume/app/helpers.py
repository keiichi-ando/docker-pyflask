from os import path, makedirs
import errno
import json
import logging
import logging.handlers
import settings


class MyTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """App log を app_path/log(sub folder)に出力するための wrapper class

    Args:
        logging (logging.handlers.TimedRotatingFileHandler): [description]
    """

    def __init__(self, filename, *args, **kwargs):
        _logfile = path.join(settings.APP_PATH, 'log', str(path.basename(filename)))
        self.mkdir_p(path.dirname(_logfile))
        super().__init__(_logfile, *args, **kwargs)

    def mkdir_p(self, path):
        """http://stackoverflow.com/a/600612/190597 (tzot)"""
        try:
            makedirs(path, mode=0o777, exist_ok=True)  # Python>3.2
        except TypeError:
            try:
                makedirs(path)
            except OSError as exc:  # Python >2.5
                if exc.errno == errno.EEXIST and path.isdir(path):
                    pass
                else:
                    raise


def is_json(request_body) -> bool:
    """ JSON形式のデータ判定 (for http request)

    Args:
        myjson (): 

    Returns:
        bool: 
    """
    try:
        _ = json.loads(request_body)
    except ValueError as e:
        return False
    return True

