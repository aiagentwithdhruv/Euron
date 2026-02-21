"""
Standalone authentication script for Google Sheets API.
Run this once to generate token.json before using the MCP server.
"""

import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(DIR_PATH, "token.json")
CREDENTIALS_PATH = os.path.join(DIR_PATH, "credentials.json")


def authenticate():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                print(f"Error: credentials.json not found in {DIR_PATH}")
                print("Download it from Google Cloud Console → APIs & Services → Credentials.")
                return
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())

    print(f"Authentication successful. Token saved to {TOKEN_PATH}")


if __name__ == "__main__":
    authenticate()
