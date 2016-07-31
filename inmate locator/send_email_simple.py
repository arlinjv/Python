import smtplib
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("sfinvestigationtools", "15851585")
 
msg = "TEST MESSAGE!"
server.sendmail("sfinvestigationtools", "arlinjv@gmail.com", msg)
server.quit()
