import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import datetime

def send_mail(send_from, send_to, subject, text, files=[], server="mailhub.lss.emc.com"):
	assert isinstance(send_to, list)
	assert isinstance(files, list)

	msg = MIMEMultipart()
	msg['From'] = send_from
	msg['To'] = COMMASPACE.join(send_to)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = subject

	msg.attach( MIMEText(text) )

	for f in files:
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open(f,"rb").read() )
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
		msg.attach(part)

	smtp = smtplib.SMTP(server,25)
	smtp.sendmail(send_from, send_to, msg.as_string())
	smtp.close()


send_from = 'donotreply@emc.com' #sender

send_to = ['uma.arunagiri@emc.com',
			'ganpat.agarwal@emc.com',
			'rekha.dilip@emc.com',
			'anupama.vainipetta@emc.com'] #recipient's list
			
#send_to = ['ganpat.agarwal@emc.com',]

subject = 'PIE Birthday Notification'
text = 'HAPPY BIRTHDAY'

#Storing today's date
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
month = str(tomorrow.month)
day = str(tomorrow.day)

filename = 'C:\PIE_Birthday_reminder\Birthdays.csv'
data = open (filename,'r')

#Parsing each line of the file and checking with today's date
for line in data:
	line_details = line.split(',')
	if line_details[0] == month:
		if line_details[1] == day:
			#setting up text
			text = "Wish Happy birthday tomorrow to : %s"%line_details[2]
				
			#sending the mail to recipients' list
			send_mail(send_from, send_to, subject, text)
			
			