from flask import Flask, jsonify, request
from mailProviders.failsafe_email_provider import FailSafeEmailProvider
from mailProviders import message
import logging
import os
app = Flask(__name__)


logger = logging.getLogger('email_Service')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

@app.route('/', methods = ['GET'])
def root():
  return jsonify({'message':'success'}), 200

@app.route('/sendMail', methods = ['POST'])
def send():
    #2. Get the mail object
    request_json = request.get_json()
    logger.debug('request_json')
    requestMessage = message.get_message(request_json)
    logger.info('request_message %s', requestMessage)
    #3. validate the input message to be non empty and valid
    if not requestMessage.validate():
        return jsonify({'status':'400',
                       'message':'BadRequest. Malformed Request'}), 400
    #4. call the email base class to send email
    emailClient = FailSafeEmailProvider()
    successful, mail_provider_name, id = emailClient.send(requestMessage)
    logger.info('response received %s', mail_provider_name)
    #5. validate response
    if not successful:
        return jsonify({'status':'503',
                       'message':'ServiceUnavailable. Unresponsive Email Providers. Try after sometime'}), 503

    return jsonify({'message':'success', 'provider': mail_provider_name, 'id': id}), 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
