import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

YT_SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]


def main():
    creds = None
    dir_path = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(dir_path, "token.json")
    creds_path = os.path.join(dir_path, "credentials.json")

    if not os.path.exists(creds_path):
        print(f"ERROR: {creds_path} not found!")
        print("Download your OAuth 2.0 Client ID JSON from Google Cloud Console")
        print("and save it as 'credentials.json' in this folder.")
        return

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, YT_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, YT_SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    print("\nAuthentication successful!")
    print(f"Token saved to {token_path}")
    print("The Social Media MCP server can now use YouTube API with this token.")


if __name__ == "__main__":
    main()
