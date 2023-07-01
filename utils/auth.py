from google_auth_oauthlib.flow import InstalledAppFlow


def authenticate_google_user():
    """Authenticate the user with the given GmailID using the credentials from the JSON file and return the GmailID and credentials."""
    gmail_id = input("Enter your Gmail ID: ")

    # Authenticate using the credentials from the JSON file
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", ["https://www.googleapis.com/auth/gmail.modify"]
    )
    creds = flow.run_local_server(port=8080)

    print("Authenticated!")

    return gmail_id, creds
