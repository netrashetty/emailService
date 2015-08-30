__author__ = 'netra.shetty'
import logging
from exceptionHandler import BadRequestException
logger = logging.getLogger('email_Service')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class Message:
    def __init__(self, to, to_name, from_name, from_email_id, cc, bcc, subject, text, headers, html):
        self.to = to
        self.to_name = to_name
        self.from_name = from_name
        self.from_email_id = from_email_id
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.text = text
        self.headers = headers
        self.html = html

    def __str__(self):
        return "self.to"+self.to+" self.from_name"+self.from_name

    def validate(self):
        if self.to is None or self.from_email_id is None or self.subject is None:
            return False
        return True



def get_message(message):
    """
    constructs the mail message with the required keys. if mandatory keys are missing, it will return None.
    """
    logger.error('inside getmessage')
    #return Message(json['to'], json['from'], json['cc'], json['bcc'], json['subject'],
    #                   json['text'], json['headers'], json['html'])
    to = None
    to_name = None
    from_name = None
    from_email_id = None
    subject = None
    text = None
    cc = None
    bcc = None
    headers = None
    html = None
    if 'to' in message:
        to = message['to']
    if 'to_name' in message:
        to_name = message['to_name']
    if 'from_name' in message:
        from_name = message['from_name']
    if 'from_email_id' in message:
        from_email_id = message['from_email_id']
    if 'subject' in message:
        subject = message['subject']
    if 'text' in message:
        text = message['text']
    if 'cc' in message:
        cc = message['cc']
    if 'bcc' in message:
        bcc = message['bcc']
    if 'headers' in message:
        headers = message['headers']
    if 'html' in message:
        html = message['html']
    return Message(to, to_name, from_name, from_email_id,
                   cc, bcc, subject,
                       text, headers, html)