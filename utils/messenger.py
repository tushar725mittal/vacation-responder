from googleapiclient.errors import HttpError


def create_message(to, subject, message_text, in_reply_to=None, references=None):
    """Prepares a message in MIME format for an email and returns the encoded form of it."""
    from email.mime.text import MIMEText
    from base64 import urlsafe_b64encode

    message = MIMEText(message_text)
    message["to"] = to
    message["subject"] = "RE:" + subject
    # Check if the email is a reply to another email or there are references to other emails
    if in_reply_to:
        message["In-Reply-To"] = in_reply_to
    if references:
        message["References"] = references

    return urlsafe_b64encode(message.as_bytes()).decode()


def send_message(service, user_id, message):
    """Sends an email message and returns the message ID."""
    try:
        message = (
            service.users().messages().send(userId=user_id, body=message).execute()
        )
        print("The email has been replied to!!")
    except HttpError as error:
        print(f"An error occurred: {error}")
        message = None

    return message
