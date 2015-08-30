#EmailService

##Problem Statement
Create a service that accepts the necessary information and sends emails. It should provide an abstraction between two different email service providers. If one of the services goes down, your service can quickly failover to a different provider without affecting your customers.

##Solution:
I implemented this using Flask framework. This service acts as a wrapper around mailgun and mandrill mail providers. The failover order for mailproviders
is MailGun followed by Mandrill.

###Exposed API:
* **POST /sendMail**
* Input request content-type: application/json
* **Example:**
* Request:

*
curl -i -H "content-type: application/json" -X POST -d'{"to": "netra.shetty@gmail.com", "from_name": "arunabh", "from_email_id":"arunabh.777@gmail.com", "subject" : "hello"}' "http://localhost:7777/sendMail"

* Response
*
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 111
Server: Werkzeug/0.10.4 Python/2.7.5
Date: Sun, 30 Aug 2015 13:28:27 GMT

{
  "id": "3d7b6d946e2240269e9196b13cfd5483", 
  "message": "success", 
  "provider": "MandrillEmailProvider"
}

###Design:
I have tried designing the service to allow for seamless onboarding of any new mailprovider. 
To enable this, i have written an abstract base class for the mail provider which all mailproviders are supposed to implement. 
I have implemented a message class that will hold all details of the message to send.

Each MailProvider class can then implement the way to send the message independently. 
There is a class FailsafeMailProvider that handles the failover logic and calling the mailproviders.
The main class is EmailService that accepts the incoming request, creates a message object, invokes the FailSafeMailProvider and outputs relevenat response.

###Todos:
The following are the list of features yet to be implemented:

1. Ability to send mail to multiple recepients (to/cc/bcc)
2. Ability to send an attachment in the email
3. Case where the email was sent successful but my emailService failed before sending out a response. This would be a tricky case to
handle, could use a message queue that can be persisted and response retried. additionally, an ability to identify if client is sending
the same request again, possibly by using an identifier. This would help ensure that the email service does not send same mail twice.
4. a more robust input validation: since the mail providers also handle validation at their end, i did not add much to the email service.
5. ability to process parallel request by emailservice
6. async processing by mailProviders (mailGun has an argument called async).
7. metrics
8. robust testing.  
