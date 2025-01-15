from flask import Flask, request, jsonify
from auth import get_gmail_service
from sender import send_email
from utils import read_message_body

app = Flask(__name__)

@app.route('/send_emails', methods=['POST'])
def send_emails():
    data = request.json
    user_email = data['user_email']
    subject = data['subject']
    body = data['body']
    recipients = data['recipients']  # List of email addresses
    attachment_path = data.get('attachment_path', None)

    service = get_gmail_service(user_email)
    results = []

    for recipient in recipients:
        try:
            send_email(
                service=service,
                sender=user_email,
                sender_name="Your Name",
                to=recipient,
                subject=subject,
                body=body,
                file_path=attachment_path,
                include_attachment=bool(attachment_path)
            )
            results.append({'recipient': recipient, 'status': 'sent'})
        except Exception as e:
            results.append({'recipient': recipient, 'status': 'failed', 'error': str(e)})

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)