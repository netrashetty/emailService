__author__ = 'netra.shetty'

import mandrill, config
from .base_email_provider import BaseEmailProvider
from exceptionHandler import ServerException
from flask import jsonify
import logging

mandrill_client = mandrill.Mandrill(config.MANDRILL_API_KEY)
logger = logging.getLogger('simple_email')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('error.log')
fh.setLevel(logging.ERROR)
logger.addHandler(fh)

class MandrillEmailProvider(BaseEmailProvider):
    name = 'MandrillEmailProvider'
    def send(self, message):
        content = {
            'from_name' : message.from_name,
            'from_email' : message.from_email_id,
            'subject' : message.subject,
            'text': message.text,
            'to': [{'email': message.to, 'name': message.to_name, 'type':'to'}]
        }
        response = None
        try:
            response = mandrill_client.messages.send(message=content, async=False, ip_pool='Main Pool')
            logger.info('Response received mandrill %s', response)
        except mandrill.Error as e:
            #log correct server exception
            raise ServerException(504, e.message)

        response = response[0]
        if response['status']=='sent':
            return response['_id']
        elif response['status']=='rejected':
            #log rejection
            raise ServerException(response['status_code'], {})
        else:
            #log failure
            return ServerException(504, "failed to send message")
