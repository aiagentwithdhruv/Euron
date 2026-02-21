import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

def main():
    """Authenticates with Google Calendar API and generates token.json."""
    creds = None
    DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    TOKEN_PATH = os.path.join(DIR_PATH, "token.json")
    CREDS_PATH = os.path.join(DIR_PATH, "credentials.json")

    if not os.path.exists(CREDS_PATH):
        print(f"ERROR: {CREDS_PATH} not found!")
        print("Please download your OAuth 2.0 Client ID JSON file from Google Cloud Console")
        print("and save it as 'credentials.json' in this folder before running this script.")
        return

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    print("\n✅ Authentication successful!")
    print(f"✅ {TOKEN_PATH} has been generated or refreshed.")
    print("The MCP server can now authenticate using this token.json file automatically.")

if __name__ == "__main__":
    main()
