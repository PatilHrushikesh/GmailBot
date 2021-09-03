from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from apiclient import errors
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify']

link="https://mail.google.com/mail/u/0/#inbox/"

def Get_Service():
	"""Shows basic usage of the Gmail API.
	Lists the user's Gmail labels.
	"""
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
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	service = build('gmail', 'v1', credentials=creds)
	return service
    

def ListMessages(service, user_id='me', query="", label_ids=[]):
	# print("QUERY :",query)
	"""List all Messages of the user's mailbox matching the query.

	Args:
		service: Authorized Gmail API service instance.
		user_id: User's email address. The special value "me"
		can be used to indicate the authenticated user.
		query: String used to filter messages returned.
		Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

	Returns:
		List of Messages that match the criteria of the query. Note that the
		returned list contains Message IDs, you must use get with the
		appropriate ID to get the details of a Message."""
	try:
		response = service.users().messages().list(userId=user_id,
                                            q=query, labelIds=label_ids).execute()
		# print(response)
		messages = []
		if 'messages' in response:
			messages.extend(response['messages'])

		while 'nextPageToken' in response:
			page_token = response['nextPageToken']
			response = service.users().messages().list(userId=user_id, q=query,
														pageToken=page_token).execute()
			messages.extend(response['messages'])
		# print("Messages\n\n")
		# for msg in messages:
		#    print(msg)
		return messages
	except errors.HttpError as error:
		print(f'An error occurred 1: {error}')

def Get_Mail():
	service = Get_Service()

	query = "newer_than:3d"+" AND category:forums"

	RemoveLabel = {'removeLabelIds': [], 'addLabelIds': ['Label_3']}

	MsgID = ListMessages(service,query=query)
	print("Length :",len(MsgID))
	MailList = []
	for msg in MsgID:
		message = service.users().messages().get(
			userId='me', id=msg['id']).execute()
		print("MESSAGE :",message['snippet'])
		# if 'Label_3' in message['labelIds']:
		# 	continue
		ModifyMessage(service,'me',msg['id'],RemoveLabel)#Remove UNREAD Label
		snippet = message['snippet']
		MailSubject = next(
				(sub['value'] for sub in message['payload']['headers']
				if sub['name'] == 'Subject'), "NO Suject")
		MailList.append('*'+MailSubject+'*'+"\n"+link+msg['id']+"\n"+snippet)
	return MailList


def ModifyMessage(service, user_id, msg, msg_labels):
	"""Modify the Labels on the given Message.

	Args:
		service: Authorized Gmail API service instance.
		user_id: User's email address. The special value "me"
		can be used to indicate the authenticated user.
		msg_id: The id of the message required.
		msg_labels: The change in labels.

	Returns:
		Modified message, containing updated labelIds, id and threadId.
	"""
	try:

		message = service.users().messages().modify(userId=user_id, id=msg,
													body=msg_labels).execute()
		return message
	except errors.HttpError as error:
		print(f'An error occurred 3: {error}')

MailList = Get_Mail()

if __name__ == '__main__':
	print(len(MailList))
	for mail in MailList:
		print(mail, "\n\n")
