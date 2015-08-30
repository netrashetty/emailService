__author__ = 'netra.shetty'

import logging
import requests, config
from .message import Message
from exceptionHandler import ClientException, ServerException, BadRequestException
logger = logging.getLogger('simple_email')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('error.log')
fh.setLevel(logging.ERROR)
logger.addHandler(fh)

class MailGunEmailProvider():
    name = 'MailGunEmailProvider'


    def __init__(self, debug=False):
        if debug:
            logger.handlers = []
            logger.addHandler(logging.StreamHandler())
            logger.setLevel(logging.DEBUG)

    def send(self, message):
        mailgun_url = config.MAILGUN_URL
        auth_api_keyname = config.MAILGUN_AUTH_API_KEYNAME
        auth_api_key = config.MAILGUN_AUTH_API_KEYVALUE
        logger.error("fromname %s", message)
        from_info = message.from_name + '<' + message.from_email_id + '>'
        r = requests.post(
            mailgun_url,
            auth=(auth_api_keyname, auth_api_key),
            data={"from":from_info,
                  "to": message.to,
                  "subject": message.subject,
                  "text": message.text})

        logger.info("Response received %s %s", r.status_code, r.json())

        if r.status_code == 400:
            logger.error("MailGunServer returned bad request %s exception %s", r.status_code, r.json)
            raise BadRequestException(r.status_code, r.json())
        elif r.status_code > 400:
            logger.error("Encountered error at client end %s %s", r.status_code, r.json())
            raise ClientException(r.status_code, r.json())
        elif r.status_code >=500:
            logger.error("Encountered error at mailgun server end %s %s", r.status_code, r.json())
            raise ServerException(r.status_code, r.json())

        return r.json()['id']
