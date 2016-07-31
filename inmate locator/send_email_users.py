#from http://www.sapnaedu.in/send-email-through-gmail-in-python/
#original example included sending attachments.

import smtplib
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email import Encoders
import os

#Create Module
def send_email(to, subject, text):

	try:
		gmail_user = 'sfinvestigationtools'
		gmail_pwd = '15851585'

		msg = MIMEMultipart()
		msg['From'] = 'sfinvestigationtools'
		msg['To'] = ", ".join(to)
		msg['Subject'] = subject

		msg.attach(MIMEText(text))
		
		'''for file in filenames:
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(open(file, 'rb').read())
			Encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"'
			% os.path.basename(file))
			msg.attach(part)
			'''
		mailServer = smtplib.SMTP("smtp.gmail.com", 587)
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()


		mailServer.login(gmail_user, gmail_pwd)
		mailServer.sendmail(gmail_user, to, msg.as_string())
		# Should be mailServer.quit(), but that crashes...
		mailServer.close()
		print('successfully sent the mail')

	except:

		print("failed to send mail")



if __name__ == '__main__':
    #attachment_file = ['file1.txt' 'file2.txt']

    to = ['arlinjv@gmail.com'] #Multiple Email Address

    TEXT = "Hello everyone,\n"
    TEXT = TEXT + "\n"
    TEXT = TEXT + "Hope you are doing fine today.\n"
    TEXT = TEXT +  "Please review the attached documents and let me know if it looks it\n"
    TEXT = TEXT + "\n"
    TEXT = TEXT + "I would be glad to answer if you have any questions"
    TEXT = TEXT + "\n"
    TEXT = TEXT + "Thanks,\n"
    TEXT = TEXT + "Kiran"


    SUBJECT = "Testing sending using gmail"

    send_email(to, SUBJECT, TEXT)
