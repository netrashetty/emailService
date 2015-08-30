__author__ = 'netra.shetty'
import abc
import logging

logger = logging.getLogger('simple_email')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('error.log')
fh.setLevel(logging.INFO)
logger.addHandler(fh)

class BaseEmailProvider():
    __metaclass__ = abc.ABCMeta

    name = 'baseEmailProvider'

    def __init__(self, debug=True):
        if debug:
            logger.handlers = []
            logger.addHandler(logging.StreamHandler())
            logger.setLevel(logging.DEBUG)

    @abc.abstractmethod
    def send(self, message):
        return