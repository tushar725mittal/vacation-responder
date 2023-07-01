from utils import auth, responder


# main function that executes the vacation responder program
def main():
    gmail_id, creds = auth.authenticate_google_user()
    print("Your Gmail ID: ", gmail_id)
    responder.respond(
        gmail_id,
        creds,
        "I am on vacation right now. I will reply to your email when I return.",
    )


# Run the main function
if __name__ == "__main__":
    main()
