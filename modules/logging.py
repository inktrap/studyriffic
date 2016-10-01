import logging
# logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

logger = logging.getLogger('main')
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
