import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.message import EmailMessage

def send_email(sender_email, sender_password, recipient_email, subject, message, attachment_path=None):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # replace with the port for your SMTP server
    smtp_username = sender_email
    smtp_password = sender_password
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message body as HTML
    msg.attach(MIMEText(f'<div style="text-align: center;"><p style="font-size: 16px; font-weight: bold;">{message}</p></div>'))

    # Attach the file if provided
    if attachment_path:
        with open(attachment_path, 'rb') as file:
            attachment = MIMEApplication(file.read())
            attachment.add_header('Content-Disposition', 'attachment', filename=file.name)
            msg.attach(attachment)

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Login to the email account
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print("Error sending email:", str(e))

    finally:
        # Quit the SMTP server
        server.quit()

# sender_email = "galacticoderr@gmail.com"
# sender_password = "jlnw esrt tjlu bnfp"
# recipient_email = "ilovevibingtolofii@gmail.com"
# subject = "Centered Text in Email"
# message = "This is an example email with centered <strong>bold text</strong> and <span style='font-size: 18px;'>bigger font</span>."
# # attachment_path = "path/to/your/file.txt"  # Replace with the actual path or set to None if no attachment

# send_email(sender_email, sender_password, recipient_email, subject, message, attachment_path=None)