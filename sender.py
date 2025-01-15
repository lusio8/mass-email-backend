import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(service, sender, sender_name, to, subject, body, file_path=None, include_attachment=True):
    message = MIMEMultipart()
    message['To'] = to
    message['From'] = f'{sender_name} <{sender}>'
    message['Subject'] = subject

    # Aggiungi il corpo del messaggio
    msg = MIMEText(body, 'plain', 'utf-8')
    message.attach(msg)

    # Allega il file, se specificato e se include_attachment è True
    if include_attachment and file_path and os.path.isfile(file_path):
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{os.path.basename(file_path)}"'
            )
            message.attach(part)

    # Converti il messaggio in formato raw
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

    try:
        # Invia il messaggio
        response = service.users().messages().send(
            userId="me",
            body={'raw': raw_message}
        ).execute()
        print(f"Email sent to {to}")
    except Exception as error:
        print(f"Error sending email to {to}: {error}")
