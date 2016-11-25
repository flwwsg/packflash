#-*- coding: utf-8 -*-
'''
file:sendmail.py
desc: using 1150712418@qq.com to send email
'''

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# '190971120@qq.com',
MYRECEIVER = ['2319406132@qq.com']
SUCCSUBJECT = '打包完成'
SUCCBODY = '打包%s完成'

def sendMail(receiver,subject,fname=None,mbody=None,server=None):
	if not server:
		server=dict()
		server['host'] ='smtp.qq.com'
		server['usr'] = '1150712418@qq.com'
		server['pwd'] = 'yarqzodyzfakggja'
		server['port'] = 465

	encode = 'utf-8'
	msg = MIMEMultipart()
	if not mbody:
		mbody = MIMEText('Python email', 'plain', encode)
	else:
		mbody = MIMEText(mbody,'plain',encode)
	msg.preamble = 'You will not see this in a MIME-aware mail reader'
	msg['From'] = server['usr']
	msg['To'] = receiver
	msg['Subject'] = subject
	
	if fname:
		att = MIMEText(open(fname,'rb').read(),'base64',encode)
		att.add_header('Content-Disposition', 'attachment', filename=fname)
		msg.attach(att)

	msg.attach(mbody)

	try:
		smail = smtplib.SMTP_SSL(server['host'], 465)
		smail.login(server['usr'], server['pwd'])
		# smail.send_message(msg)
		smail.sendmail(server['usr'], receiver, msg.as_string())
		# print('Email send successful')
	except smtplib.SMTPException:
		print('Failing to send email' )
	finally:
		smail.quit()



