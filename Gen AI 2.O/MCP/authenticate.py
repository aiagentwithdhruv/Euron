import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://mail.google.com/"
]

def main():
    """Shows basic usage of the Gmail API.
    Prints the user's labels, and generates a token.json for the MCP server.
    """
    creds = None
    DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    TOKEN_PATH = os.path.join(DIR_PATH, "token.json")
    CREDS_PATH = os.path.join(DIR_PATH, "credentials.json")

    if not os.path.exists(CREDS_PATH):
        print(f"ERROR: {CREDS_PATH} not found!")
        print("Please download your OAuth 2.0 Client ID JSON file from Google Cloud Console")
        print("and save it as 'credentials.json' in this folder before running this script.")
        return

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
            
    print("\n✅ Authentication successful!")
    print(f"✅ {TOKEN_PATH} has been generated or refreshed.")
    print("The MCP server can now authenticate using this token.json file automatically.")

if __name__ == "__main__":
    main()
