import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import os

# Set your email login credentials
sender_email = "example@gmail.com"
sender_password = "your password"

# Set the email message and subject
subject = "YOUR  WORKSHOP CERTIFICATE"
body = "Dear participant,\n\nPlease find attached your digital certificate for completing our workshop.\n\nBest regards,\n\n Your Name"

# Set the list of recipients and their names
recipients = {"name1@gmail.com":   "name1",
              "name2@gmail.com":  "name2",
              ......
              "name30@outlook.fr":  "name30"
              }

# Set the path to the digital certificate file
certificate_paths = ['something/filename.pdf',
                     'something/filename2.pdf',
                     ..........
                     'something/filename30.pdf'
                     ]

# Loop through recipients and send separate emails with attached certificates
for recipient_email, recipient_name in recipients.items():
    # Create a new email message for each recipient
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f'{subject} - {recipient_name}'
    msg.attach(MIMEText(body, 'plain'))

    # Find the corresponding certificate path for the current recipient
    certificate_path = certificate_paths.pop(0)  # Pop the first certificate path from the list
    with open(certificate_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename(certificate_path)  # Extract only the filename
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        msg.attach(part)

    # Send the email to the current recipient
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

print("Emails sent successfully!")

