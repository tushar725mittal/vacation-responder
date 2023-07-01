import time
import random
from utils import messenger
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def respond(gmail_id, creds, reply_message, time_interval=[45, 120]):
    """Respond to emails in the inbox of the Gmail account with the given GmailID using the credentials from the JSON file."""
    try:
        print("Checking your emails...")
        # Create Gmail API service instance
        service = build("gmail", "v1", credentials=creds)

        # Set the label name for replied emails
        label_name = "Replied"

        # Creates the label if it doesn't exist to be applied to the replied emails
        labels = service.users().labels().list(userId=gmail_id).execute()
        label_id = None
        for label in labels["labels"]:
            if label["name"] == label_name:
                label_id = label["id"]
                break
        if not label_id:
            label = {"name": label_name}
            created_label = (
                service.users().labels().create(userId=gmail_id, body=label).execute()
            )
            label_id = created_label["id"]

        # Set the auto-reply message
        reply_message = reply_message

        while True:
            # Get all unread emails from the inbox
            unread_emails = (
                service.users()
                .messages()
                .list(userId=gmail_id, q="is:unread")
                .execute()
            )

            # Reply to each email and add the label
            for email in unread_emails.get("messages", []):
                email_id = email["id"]
                email_data = (
                    service.users()
                    .messages()
                    .get(userId=gmail_id, id=email_id)
                    .execute()
                )
                payload = email_data["payload"]
                headers = payload["headers"]
                # Get the subject and sender of the email
                subject = next(
                    (i["value"] for i in headers if i["name"].lower() == "subject"),
                    "No Subject",
                )  # Using next so that a default value "No Subject" is returned if the subject is empty

                sender = [i["value"] for i in headers if i["name"].lower() == "from"][0]

                # Get the thread ID of the email
                email_thread_id = email_data["threadId"]

                # Check if the email has already been replied to be checking if the replied label has been applied
                replied = label_id in email_data["labelIds"]

                # Reply to the email and add the label if it hasn't been replied to yet
                if not replied:
                    # Get the Message-ID of the original email
                    message_id = next(
                        (
                            i["value"]
                            for i in headers
                            if i["name"].lower() == "message-id"
                        ),
                        None,
                    )
                    body = {
                        "raw": messenger.create_message(
                            sender,
                            subject,
                            reply_message,
                            in_reply_to=message_id,
                            references=message_id,
                        )
                    }
                    body["threadId"] = email_thread_id
                    send_response = messenger.send_message(service, gmail_id, body)
                    if send_response:
                        # Show the subject of the email that has been replied to
                        print(f"Replied to: {subject} from {sender}.")
                    service.users().messages().modify(
                        userId=gmail_id, id=email_id, body={"addLabelIds": [label_id]}
                    ).execute()

            # Wait for a random interval between 45 and 120 seconds before checking for new emails again
            time.sleep(random.randint(time_interval[0], time_interval[1]))

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
