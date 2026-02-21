import os
from datetime import datetime, timedelta, timezone
from mcp.server.fastmcp import FastMCP

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

mcp = FastMCP("Google Calendar MCP Server")

SCOPES = ["https://www.googleapis.com/auth/calendar"]
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(DIR_PATH, "token.json")


def get_calendar_service():
    """Get the Google Calendar API service instance using OAuth 2.0 credentials."""
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
            raise ValueError("Authentication token missing or invalid. Please run 'python authenticate.py' first.")

    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except Exception as e:
        raise ValueError(f"Failed to build Calendar service: {e}")


def _format_event(event: dict) -> str:
    """Format a single calendar event into a readable string."""
    summary = event.get("summary", "(No title)")
    event_id = event.get("id", "N/A")
    location = event.get("location", "")
    description = event.get("description", "")

    start = event.get("start", {})
    end = event.get("end", {})
    start_str = start.get("dateTime", start.get("date", "Unknown"))
    end_str = end.get("dateTime", end.get("date", "Unknown"))

    lines = [
        f"📅 {summary}",
        f"   ID: {event_id}",
        f"   Start: {start_str}",
        f"   End:   {end_str}",
    ]
    if location:
        lines.append(f"   Location: {location}")
    if description:
        preview = description[:200] + "..." if len(description) > 200 else description
        lines.append(f"   Description: {preview}")

    return "\n".join(lines)


@mcp.tool()
def list_events(limit: int = 10, days_ahead: int = 7) -> str:
    """List upcoming calendar events in the next N days."""
    try:
        service = get_calendar_service()

        now = datetime.now(timezone.utc)
        time_max = now + timedelta(days=days_ahead)

        results = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now.isoformat(),
                timeMax=time_max.isoformat(),
                maxResults=limit,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = results.get("items", [])

        if not events:
            return f"No upcoming events in the next {days_ahead} day(s)."

        formatted = [_format_event(e) for e in events]
        header = f"Found {len(events)} event(s) in the next {days_ahead} day(s):\n"
        return header + "\n---\n".join(formatted)
    except Exception as e:
        return f"Failed to list events: {str(e)}"


@mcp.tool()
def create_event(
    summary: str,
    start_datetime: str,
    end_datetime: str,
    description: str = "",
    location: str = "",
) -> str:
    """
    Create a new Google Calendar event.
    Start and end must be in ISO 8601 format, e.g. '2026-02-22T10:00:00'.
    A local timezone offset is added automatically if none is provided.
    """
    try:
        service = get_calendar_service()

        def _ensure_tz(dt_str: str) -> str:
            if "Z" not in dt_str and "+" not in dt_str and "-" not in dt_str[10:]:
                local_offset = datetime.now(timezone.utc).astimezone().strftime("%z")
                offset_formatted = local_offset[:3] + ":" + local_offset[3:]
                return dt_str + offset_formatted
            return dt_str

        event_body: dict = {
            "summary": summary,
            "start": {"dateTime": _ensure_tz(start_datetime)},
            "end": {"dateTime": _ensure_tz(end_datetime)},
        }
        if description:
            event_body["description"] = description
        if location:
            event_body["location"] = location

        created = service.events().insert(calendarId="primary", body=event_body).execute()
        return (
            f"Event created successfully!\n"
            f"  Title: {created.get('summary')}\n"
            f"  ID: {created.get('id')}\n"
            f"  Link: {created.get('htmlLink')}"
        )
    except Exception as e:
        return f"Failed to create event: {str(e)}"


@mcp.tool()
def search_events(query: str, limit: int = 10) -> str:
    """
    Search calendar events by text query.
    Searches across event titles, descriptions, and locations.
    """
    try:
        service = get_calendar_service()

        now = datetime.now(timezone.utc)

        results = (
            service.events()
            .list(
                calendarId="primary",
                q=query,
                timeMin=now.isoformat(),
                maxResults=limit,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = results.get("items", [])

        if not events:
            return f"No events found matching '{query}'."

        formatted = [_format_event(e) for e in events]
        header = f"Found {len(events)} event(s) matching '{query}':\n"
        return header + "\n---\n".join(formatted)
    except Exception as e:
        return f"Failed to search events: {str(e)}"


@mcp.tool()
def delete_event(event_id: str) -> str:
    """Delete a calendar event by its event ID."""
    try:
        service = get_calendar_service()
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return f"Event '{event_id}' deleted successfully."
    except Exception as e:
        return f"Failed to delete event: {str(e)}"


@mcp.tool()
def get_todays_schedule() -> str:
    """Get all calendar events scheduled for today."""
    try:
        service = get_calendar_service()

        local_now = datetime.now().astimezone()
        start_of_day = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        results = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_of_day.isoformat(),
                timeMax=end_of_day.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = results.get("items", [])

        today_str = local_now.strftime("%A, %B %d, %Y")
        if not events:
            return f"No events scheduled for today ({today_str})."

        formatted = [_format_event(e) for e in events]
        header = f"Today's schedule — {today_str} ({len(events)} event(s)):\n"
        return header + "\n---\n".join(formatted)
    except Exception as e:
        return f"Failed to get today's schedule: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
