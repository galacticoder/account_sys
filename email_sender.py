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
    
    with open("C:\\Users\\zombi\\OneDrive\\Desktop\\system_proj\\templates\\temp\\index.html","r") as temp:
        content = temp.read()
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    html_temp = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email-Verification</title>
        <style>        
        .email-text {{
            text-align: center;
        }}

        .logo-container {{
            text-align: center;
        }}

        .logo {{
            height: 25px;
            width: 25px;
            border-radius: 50%;
        }}
        </style>
    </head>
    <body>
        <h1 class='email-text'>{message}</h1>
        <div class='logo-container'>
            <a href='https://github.com/galacticoder'>
                <img src="https://cdn.pixabay.com/photo/2022/01/30/13/33/github-6980894_1280.png" class='logo'/>
            </a>
        </div>
    </body>
    </html>
    """


    
    msg.attach(MIMEText(html_temp, 'html'))

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