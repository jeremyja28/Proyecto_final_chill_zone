import logging
import os
from config import Config

_logger = None

def get_logger():
    global _logger
    if _logger:
        return _logger

    os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
    logger = logging.getLogger('sgcz')
    logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))

    fh = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    _logger = logger
    return _logger
