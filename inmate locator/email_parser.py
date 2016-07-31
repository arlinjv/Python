server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
server.ehlo()
server.starttls()
gmail_user = 'sfinvestigationtools'
gmail_pwd = '15851585'
server.login(gmail_user, gmail_pwd)
