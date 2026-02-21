import os
import base64
from email.message import EmailMessage
from mcp.server.fastmcp import FastMCP

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

mcp = FastMCP("Email Automation Server (Gmail API)")

SCOPES = ["https://mail.google.com/"]
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(DIR_PATH, "token.json")

def get_gmail_service():
    """Get the Gmail API service instance using OAuth 2.0 credentials."""
    creds = None
    
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(TOKEN_PATH, "w") as token:
                    token.write(creds.to_json())
            except Exception as e:
                raise ValueError(f"Failed to refresh token: {e}. Please run authenticate.py again.")
        else:
            raise ValueError(f"Authentication token missing or invalid. Please run 'python authenticate.py' first.")
            
    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except Exception as e:
        raise ValueError(f"Failed to build Gmail service: {e}")

def _extract_body_text(parts):
    """Helper to extract text/plain from nested payload parts."""
    text_content = ""
    if not parts:
        return text_content
    for part in parts:
        if part.get('mimeType') == 'text/plain':
            data = part.get('body', {}).get('data')
            if data:
                text_content += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        elif 'parts' in part:
            text_content += _extract_body_text(part['parts'])
    return text_content

@mcp.tool()
def send_email(to_email: str, subject: str, body: str) -> str:
    """Send an email to a specific address using the Gmail API."""
    try:
        service = get_gmail_service()
        
        message = EmailMessage()
        message.set_content(body)
        message['To'] = to_email
        message['Subject'] = subject
        
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}
        
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        return f"Successfully sent email to {to_email}. Message Id: {send_message['id']}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

@mcp.tool()
def read_recent_emails(limit: int = 5, query: str = "") -> str:
    """
    Read the most recent emails using Gmail API. 
    Optional 'query' parameter uses standard Gmail search syntax (e.g., 'is:unread', 'from:boss@example.com').
    """
    try:
        service = get_gmail_service()
        
        results = service.users().messages().list(userId='me', maxResults=limit, q=query).execute()
        messages = results.get('messages', [])
        
        if not messages:
            return "No emails found."
            
        parsed_emails = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            
            payload = msg['payload']
            headers = payload.get('headers', [])
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")
            date = next((h['value'] for h in headers if h['name'] == 'Date'), "Unknown Date")
            
            # Extract body
            body = "No text body found."
            
            if 'parts' in payload:
                body = _extract_body_text(payload['parts'])
            elif payload.get('mimeType') == 'text/plain':
                data = payload.get('body', {}).get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            
            body_preview = body[:300] + "..." if len(body) > 300 else body
            parsed_emails.append(f"From: {sender}\nDate: {date}\nSubject: {subject}\nBody preview:\n{body_preview}\n")
            
        return "\n---\n".join(parsed_emails)
    except Exception as e:
        return f"Failed to read emails: {str(e)}"

@mcp.tool()
def search_emails(query: str, limit: int = 5) -> str:
    """
    Search emails using standard Gmail search query syntax.
    Examples:
    - 'from:example@example.com'
    - 'subject:meeting'
    - 'is:unread in:inbox'
    - 'after:2026/01/01'
    """
    return read_recent_emails(limit=limit, query=query)

@mcp.tool()
def mark_email_seen(query: str) -> str:
    """
    Mark emails matching a specific Gmail search query as read.
    Make sure to include 'is:unread' in your query.
    Example query: 'from:boss@example.com is:unread'
    """
    try:
        service = get_gmail_service()
        
        # Ensure we only fetch unread emails if the user didn't specify it
        if "is:unread" not in query.lower():
            query += " is:unread"
            
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        
        if not messages:
            return f"No unread emails found matching query: {query}"
            
        count = 0
        for message in messages:
            service.users().messages().modify(
                userId='me', 
                id=message['id'], 
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            count += 1
            
        return f"Successfully marked {count} email(s) as read."
    except Exception as e:
        return f"Failed to mark emails as seen: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
