__author__ = 'netra.shetty'

class ServerException():
    '''Error thrown by mail provider servers'''
    def __init__(self, statuscode, errormessage):
        self.error_message = errormessage
        self.status_code = statuscode

class BadRequestException():
    '''malformed request'''
    def __init__(self, statuscode, errormessage):
        self.error_message = errormessage
        self.status_code = statuscode

class ClientException():
    '''exception encountered due to issues with the client'''
    def __init__(self, statuscode, errormessage):
        self.error_message = errormessage
        self.status_code = statuscode