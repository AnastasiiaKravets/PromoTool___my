from __future__ import print_function
import random
import base64
import httplib2
import os

import time
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from html.parser import HTMLParser


def new_user_email():
    randomizer = random.randint(1, 89405)
    email = 'globuspromotool+' + str(randomizer) + '@gmail.com'
    return email


class MyHTMLParser(HTMLParser):
    href = None

    """Get url from html"""

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                self.href = attr


flags = None

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_link_from_mail():
    """
    Creates a Gmail API service object.
    Read all messages from inbox.
    Get html data from last unreaded message
    Get link from message body
    Return link
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    try:
        response = service.users().messages().list(userId='me',
                                                   labelIds='INBOX').execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me',
                                                       labelIds='INBOX',
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])
            # print('messages', messages)
    except Exception as error:
        print('An error occurred: %s' % error)
    for i in range(20):
        if len(messages) == 0:
            time.sleep(1)
        else:
            last_message_id = messages[0]['id']
            break
        if i == 19:
            raise Exception('Email was not recieved')
    message = service.users().messages().get(userId='me', id=last_message_id, format='full').execute()
    data = base64.urlsafe_b64decode(message['payload']['body']['data'])
    # print(data)
    parser = MyHTMLParser()
    parser.feed(str(data))
    delete_message(msg_id=last_message_id, service=service)
    return parser.href[1]


def delete_message(msg_id, service, user_id='me'):
    """Delete a Message.
  Args:
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message to delete.
  """
    try:
        service.users().messages().delete(userId=user_id, id=msg_id).execute()
        print('Message with id: {} deleted successfully.'.format(msg_id))
    except Exception as error:
        print('An error occurred: {}'.format(error))
