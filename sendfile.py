# Generic send files by mail
import os
import email, smtplib, ssl 
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def sendFiles(SERVER,FROM,TO,SUBJECT,BODY,FILENAMES,port=25 , username='', password='', use_tls=False):

    # Prepare actual message
    message = MIMEMultipart()
    message["From"] = FROM
    message["To"] = COMMASPACE.join(TO)
    message["Date"] =  formatdate(localtime=True)
    message["Subject"] = SUBJECT
    message["Bcc"] = COMMASPACE.join(TO)
    message.attach(MIMEText(BODY))

    # prepare attachments
    for f in FILENAMES or []:
        with open(f, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name= basename(f))
        part['Content-Disposition'] = f"attachment; filename= {basename(f)}"
        message.attach(part)    

    # Send the mail
    server = smtplib.SMTP(SERVER,port)
    if use_tls:
        server.starttls()
        server.login(username,password)

    server.sendmail(FROM, TO, message.as_string())
    server.quit()


if __name__ == "__main__":

    SERVER     = "yoursmtp.domain.org"
    PORT       = 25
    USE_TLS    = False
    USERNAME   = "put your username" # Also TLS needs to be True to authenticate
    PASSWORD   = "put your password"
    FROM       = 'noreply@domain.org'
    TO         = ["email1@domain.org", "email2@domain.org"] # must be a list
    SUBJECT    = "This is a test subject"
    BODY       = "This is a message test with attached files."
    FILEATTACH = [os.path.join("output", file) for file in os.listdir("output")]
 
    
    sendFiles(SERVER,FROM,TO,SUBJECT,BODY,FILEATTACH,PORT,USERNAME, PASSWORD, USE_TLS )
    
