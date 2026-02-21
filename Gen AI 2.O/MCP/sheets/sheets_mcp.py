import os
import json

from mcp.server.fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(DIR_PATH, "token.json")
CREDENTIALS_PATH = os.path.join(DIR_PATH, "credentials.json")

mcp = FastMCP("Google Sheets")


def get_sheets_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(
                    f"credentials.json not found in {DIR_PATH}. "
                    "Download it from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return build("sheets", "v4", credentials=creds)


@mcp.tool()
def read_sheet(spreadsheet_id: str, range_name: str = "Sheet1") -> str:
    """Read data from a Google Sheets spreadsheet range (e.g. "Sheet1!A1:D10"). Returns a formatted table."""
    try:
        service = get_sheets_service()
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        rows = result.get("values", [])
        if not rows:
            return "No data found in the specified range."

        col_widths = []
        for col_idx in range(max(len(row) for row in rows)):
            width = max(
                (len(str(row[col_idx])) if col_idx < len(row) else 0)
                for row in rows
            )
            col_widths.append(max(width, 3))

        lines = []
        for i, row in enumerate(rows):
            padded = [
                str(row[j]).ljust(col_widths[j]) if j < len(row) else " " * col_widths[j]
                for j in range(len(col_widths))
            ]
            lines.append("| " + " | ".join(padded) + " |")
            if i == 0:
                lines.append("| " + " | ".join("-" * w for w in col_widths) + " |")

        return f"Found {len(rows)} rows:\n\n" + "\n".join(lines)
    except Exception as e:
        return f"Error reading sheet: {e}"


@mcp.tool()
def write_to_sheet(spreadsheet_id: str, range_name: str, values: str) -> str:
    """Write data to a Google Sheets range. `values` is a JSON string of a 2D array, e.g. '[["Name","Age"],["John","30"]]'."""
    try:
        data = json.loads(values)
        if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
            return "Error: values must be a JSON 2D array, e.g. '[[\"a\",\"b\"],[\"c\",\"d\"]]'"

        service = get_sheets_service()
        body = {"values": data}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        updated = result.get("updatedCells", 0)
        return f"Successfully wrote {updated} cells to {range_name}."
    except json.JSONDecodeError:
        return "Error: Could not parse values. Provide a valid JSON 2D array string."
    except Exception as e:
        return f"Error writing to sheet: {e}"


@mcp.tool()
def append_to_sheet(spreadsheet_id: str, range_name: str, values: str) -> str:
    """Append rows to the end of existing data in a sheet. `values` is a JSON string of a 2D array, e.g. '[["John","30"]]'."""
    try:
        data = json.loads(values)
        if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
            return "Error: values must be a JSON 2D array, e.g. '[[\"a\",\"b\"],[\"c\",\"d\"]]'"

        service = get_sheets_service()
        body = {"values": data}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body=body,
            )
            .execute()
        )
        updates = result.get("updates", {})
        updated_rows = updates.get("updatedRows", 0)
        return f"Successfully appended {updated_rows} rows to {range_name}."
    except json.JSONDecodeError:
        return "Error: Could not parse values. Provide a valid JSON 2D array string."
    except Exception as e:
        return f"Error appending to sheet: {e}"


@mcp.tool()
def create_spreadsheet(title: str) -> str:
    """Create a new Google Sheets spreadsheet. Returns the spreadsheet ID and URL."""
    try:
        service = get_sheets_service()
        body = {"properties": {"title": title}}
        spreadsheet = service.spreadsheets().create(body=body).execute()
        sid = spreadsheet.get("spreadsheetId", "")
        url = spreadsheet.get("spreadsheetUrl", "")
        return f"Created spreadsheet \"{title}\"\nID: {sid}\nURL: {url}"
    except Exception as e:
        return f"Error creating spreadsheet: {e}"


@mcp.tool()
def list_sheets(spreadsheet_id: str) -> str:
    """List all sheet tabs in a Google Sheets spreadsheet with their names and IDs."""
    try:
        service = get_sheets_service()
        metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = metadata.get("sheets", [])
        if not sheets:
            return "No sheets found in this spreadsheet."

        lines = [f"Found {len(sheets)} sheet(s):\n"]
        for sheet in sheets:
            props = sheet.get("properties", {})
            name = props.get("title", "Untitled")
            sheet_id = props.get("sheetId", "N/A")
            index = props.get("index", "N/A")
            lines.append(f"  {index}. \"{name}\" (ID: {sheet_id})")
        return "\n".join(lines)
    except Exception as e:
        return f"Error listing sheets: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
