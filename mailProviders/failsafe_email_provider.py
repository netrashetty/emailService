__author__ = 'netra.shetty'

from .base_email_provider import BaseEmailProvider
from .mailgun_email_provider import MailGunEmailProvider
from .mandrill_email_provider import MandrillEmailProvider
from exceptionHandler import ServerException, ClientException, BadRequestException
import logging

logger = logging.getLogger('failsafe_email')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class FailSafeEmailProvider(BaseEmailProvider):
    name = 'FailSafeEmailProvider'
    email_providers = [MailGunEmailProvider, MandrillEmailProvider]

    def send(self, message):
        logger.info('entered send mail failsafe')
        #send email using first working provider
        sent = False
        for provider in FailSafeEmailProvider.email_providers:
            try:
                logger.info('calling provider %s', provider)
                id = provider().send(message)
                logger.info('received response %s from provider %s', id, provider().name)
                sent = True
                return sent, provider().name, id
            except ClientException as ce:
                logger.error('encountered client error %s at %s mailprovider', ce.error_message, provider().name)
                continue
            except ServerException as se:
                logger.error('encountered server error %s at %s mailprovider', se.error_message, provider().name)
                continue
            except BadRequestException as be:
                logger.error('encountered bad request error %s at %s mailprovider', be.error_message, provider().name)
                continue
        return sent, None, 0

