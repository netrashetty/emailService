__author__ = 'netra.shetty'

from emailService import app
import unittest

class EmailServiceTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['MANDRILL_API_KEY'] = "W1-1PEVgNBkpzsNtuc1AGw"
        app.config['MAILGUN_URL'] = "https://api.mailgun.net/v3/sandbox8a1a1c0031c94bd29a7e5aefaea105bb.mailgun.org/messages"
        app.config['MAILGUN_AUTH_API_KEYNAME'] = "api"
        app.config['MAILGUN_AUTH_API_KEYVALUE'] = "key-d89b4c81faf1e327a89dd04fe7a5fd62"
        self.app = app.test_client()
        self.app.testing = True
        self.header = {
            'content-type': 'application/json'
        }
    def send_mail(self, data):
        response = self.app.post('/sendMail', data=data, headers=self.header)
        return response

    #test bad request
    def test_reject_invalid_mailformat_request(self):
        data = {
            'to' : 'netra.shetty@gmail.com',
            'from' : 'netra.shetty@gmail.com',
        }
        response = self.send_mail(data)
        self.assertEquals(response.status_code, 400)

    def test_accept_valid_basic_mail(self):
        data = {
            'to': 'netra.shetty@gmail.com',
            'from_name': 'netra',
            'from_email_id':'netra.shetty@inmobi.com',
            'subject': 'test_accept_valid_basic_email',
            'text':'unittest text 123'
        }
        response = self.send_mail(data)
        self.assertEquals(response.status_code, 200)

    def test_fail_over(self):
        '''mailgun requires text to be provided in the mail data.
        hence would send a bad request for the following case.
        emailservice will fallback to mandrill then'''
        data = {
            'to': 'netra.shetty@gmail.com',
            'from_name': 'netra',
            'from_email_id':'netra.shetty@inmobi.com',
            'subject': 'test_accept_valid_basic_email',
        }
        response = self.send_mail(data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.provider, 'MandrillEmailProvider')

if __name__ == '__main__':
    unittest.main()