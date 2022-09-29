import os.path
import re
import email
import base64

# Import required libraries for gmail API
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.message import EmailMessage

# If modifying these scopes, delete the file token.json.
# If token.json was deleted, the refresh_token (property) will be gone too. 
# refresh_token was only generated first time to connect to Gmail API.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

# Define the app directory
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the company primary email
COMPANY_EMAIL = 'customerservice.democompany@gmail.com'

# Source code reference: Google Gmail API Python Quickstart
# https://developers.google.com/gmail/api/quickstart/python

def auth():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:            
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(APP_DIR, 'credentials.json'), SCOPES)
            creds = flow.run_local_server()  # Default port is 8080
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())   
    return creds

# This function accept one parameter which is a list of emails and refresh it
def refreshEmails(emails):
    creds = auth();

    try:
        # Connect to gmail API
        service = build('gmail', 'v1', credentials=creds)
        
        # Request a list of latest 100 (default) messages
        results = service.users().messages().list(userId='me', labelIds='INBOX').execute()
        
        # Get a list of dictionaries {"id": "", "threadID": ""}
        messages = results.get('messages', [])

        for message in messages:
            uniqueId = message['id']
            
            # Avoid duplication
            if len(emails) and uniqueId in [ sub['gmail_id'] for sub in emails ]:
                continue
            
            # Capture header and subject
            metadata = service.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
            headers = metadata['payload']['headers']
            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
                if header['name'] == 'From':
                    sender = re.search(r"\<(.+?)\>", header['value']).group(1)

            # Capture the message body
            # The body of message was encoded, we have to decode it with base 64 decoder
            raw = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
            snippet = raw['snippet']
            msg_bytes = base64.urlsafe_b64decode(raw['raw'].encode('ASCII'))
            # Get the message object from decoded bytes, using default policy
            msg_object = email.message_from_bytes(msg_bytes, policy=email.policy.default)
            # Return the current payload, which will be a list of Message objects when is_multipart() is True,
            # or a string when is_multipart() is False.
            if msg_object.is_multipart():
                body = msg_object.get_payload()[0].get_payload()
            else:
                body = msg_object.get_payload()
            
            emails.append({'gmail_id': uniqueId,
                           'subject': subject,
                           'from': sender,
                           'message': body,
                           'snippet': snippet})
      
    except HttpError as error:
        print(f'An error occurred: {error}')
        
        
def sendEmail(obj):
    creds = auth()
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content(obj["content"])

        message['To'] = obj["to"]
        message['From'] = COMPANY_EMAIL
        message['Subject'] = obj["title"]

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(f'Message was successfully sent. Id is {send_message["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}')
        send_message = None
    return send_message
    
    
        


        