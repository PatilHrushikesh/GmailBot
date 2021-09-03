# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from FetchMail import Get_Mail
import time
import schedule

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
SentFrom = os.environ['TWILIO_FROM_NUM']
SentTo = os.environ['TWILIO_TO_NUM']

def Send_msg(text):
	client = Client(account_sid, auth_token)

	message = client.messages.create(
		body=text,
		from_='whatsapp:'+SentFrom,
		to='whatsapp:'+SentTo
	)

	# print(message.sid)

def sendOnebyOne():
	# Send_msg("mail")
	MailList = Get_Mail()
	print("\nIN\n")
	for mail in MailList:
		# time.sleep(1)
		print("waiting\n")
		Send_msg(mail)
		print("\n---SENT--\n")
		# print(mail,"\n")
		time.sleep(1)

def Scheduler():
	schedule.every(10).minutes.do(sendOnebyOne)
	while True:

		# Checks whether a scheduled task
		# is pending to run or not
		schedule.run_pending()
		time.sleep(1)


Scheduler()
# if __name__ == '__main__':
# 	# Send_msg("mail")
# 	for mail in MailList:
# 		# print(mail)
# 		# Send_msg("mail")
# 		time.sleep(1)
# 		Send_msg(mail)
# 		# print("SENT\n")
# 		# time.sleep(1)
