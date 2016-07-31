import smtplib
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email import Encoders
import os


server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
server.ehlo()
server.starttls()
gmail_user = 'sfinvestigationtools'
gmail_pwd = '15851585'
server.login(gmail_user, gmail_pwd)

msg = MIMEMultipart()
to = ['arlinjv@gmail.com'] #Multiple Email Address
Subject = "Test Message"

# Message can be a simple text message or HTML
TEXT = "Hello everyone,\n"
TEXT = TEXT + "\n"
TEXT = TEXT + "Hope you are doing fine today.\n"
TEXT = TEXT +  "Please review the attached documents and let me know if it looks it\n"
TEXT = TEXT + "\n"
TEXT = TEXT + "I would be glad to answer if you have any questions"
TEXT = TEXT + "\n"
TEXT = TEXT + "Thanks,\n"
TEXT = TEXT + "Kiran"

		
msg['From'] = 'kiran.chandrashekhar@gmail.com'
msg['To'] = ", ".join(to) #Join them as we have multiple recipients
msg['Subject'] = Subject
msg.attach(MIMEText(text))

print "sending email ..."
server.sendmail(gmail_user, to, msg.as_string())
# Should be server.quit(), but that crashes...
server.close()
