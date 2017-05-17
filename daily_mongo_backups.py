from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import smtplib, os, sys, subprocess, shlex, schedule, time, datetime, json

def get_mongodump():
  '''Run a mongodump command to save the given db to disk'''
  command =  'mongodump --db ' + db_name
  subprocess.call(shlex.split(command))

def zip_mongodump():
  '''Zip up the output from a mongo dump'''
  command = 'tar -zcf dump.tar.gz dump'
  subprocess.call(shlex.split(command))

def send_mail(server='127.0.0.1'):
  '''Send an email with a mongodb attachment'''
  send_from = config['email_from_address']
  send_to = config['email_to_address']
  subject = config['email_subject']
  text = config['email_message']
  archive = 'dump.tar.gz'

  if isinstance(send_to, list):
    send_to = COMMASPACE.join(send_to)

  msg = MIMEMultipart()
  msg['From'] = send_from
  msg['To'] = send_to
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject
  msg.attach(MIMEText(text))

  with open(archive, 'rb') as filehandler:
    part = MIMEApplication( filehandler.read(), Name=os.path.basename(archive) )
    part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(archive)
    msg.attach(part)

  smtp = smtplib.SMTP(server)
  smtp.sendmail(send_from, send_to, msg.as_string())
  print('email sent at', datetime.datetime.utcnow())
  smtp.close()

if __name__ == '__main__':

  print('process started')
  
  # load the user configurations
  config = json.load(open('config.json'))

  # specify the db name and archive name, directory, and path
  db_name = config['db_name']

  # backup the db
  get_mongodump()
  zip_mongodump()

  # send the email
  schedule.every().day.at('10:00').do(send_mail)

  while 1:
    schedule.run_pending()
    time.sleep(1)
