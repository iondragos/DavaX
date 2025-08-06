import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

def setup_logger():
    logger = logging.getLogger('request_logger')
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        'logs/requests.log',
        maxBytes=5*1024*1024,   # 5 MB
        backupCount=3           # keep last 3 files
    )

    fmt = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger
