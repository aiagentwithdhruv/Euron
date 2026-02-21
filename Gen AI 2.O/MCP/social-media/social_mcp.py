import os
import json
import httpx
from mcp.server.fastmcp import FastMCP

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

mcp = FastMCP("Social Media MCP Server (YouTube + Instagram + Facebook)")

# --- YouTube Config ---
YT_SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(DIR_PATH, "token.json")

# --- Meta / Instagram / Facebook Config ---
META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN", "")
INSTAGRAM_BUSINESS_ID = os.environ.get("INSTAGRAM_BUSINESS_ID", "")
FACEBOOK_PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "")
META_API_BASE = "https://graph.facebook.com/v19.0"


# ============================================================
# YouTube Auth
# ============================================================

def get_youtube_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, YT_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(TOKEN_PATH, "w") as token:
                    token.write(creds.to_json())
            except Exception as e:
                raise ValueError(f"Failed to refresh YouTube token: {e}. Run authenticate.py again.")
        else:
            raise ValueError("YouTube auth token missing. Run authenticate.py first.")
    return build("youtube", "v3", credentials=creds)


# ============================================================
# Meta Graph API helper
# ============================================================

def meta_get(endpoint: str, params: dict | None = None) -> dict:
    params = params or {}
    params["access_token"] = META_ACCESS_TOKEN
    resp = httpx.get(f"{META_API_BASE}/{endpoint}", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def meta_post(endpoint: str, data: dict | None = None) -> dict:
    data = data or {}
    data["access_token"] = META_ACCESS_TOKEN
    resp = httpx.post(f"{META_API_BASE}/{endpoint}", data=data, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ============================================================
# YouTube Tools
# ============================================================

@mcp.tool()
def youtube_search(query: str, limit: int = 5) -> str:
    """Search YouTube videos by query. Returns title, channel, views, and URL for each result."""
    try:
        yt = get_youtube_service()
        search_resp = yt.search().list(
            part="snippet", q=query, type="video", maxResults=limit
        ).execute()

        items = search_resp.get("items", [])
        if not items:
            return f"No results found for '{query}'."

        video_ids = [item["id"]["videoId"] for item in items]
        stats_resp = yt.videos().list(
            part="statistics,snippet", id=",".join(video_ids)
        ).execute()

        results = []
        for v in stats_resp.get("items", []):
            snippet = v["snippet"]
            stats = v.get("statistics", {})
            views = int(stats.get("viewCount", 0))
            results.append(
                f"Title: {snippet['title']}\n"
                f"Channel: {snippet['channelTitle']}\n"
                f"Views: {views:,}\n"
                f"URL: https://www.youtube.com/watch?v={v['id']}"
            )
        return "\n---\n".join(results)
    except Exception as e:
        return f"YouTube search failed: {e}"


@mcp.tool()
def youtube_channel_stats(channel_id: str = "") -> str:
    """Get YouTube channel statistics (subscribers, views, video count). Leave channel_id empty for the authenticated user's channel."""
    try:
        yt = get_youtube_service()

        if channel_id:
            resp = yt.channels().list(part="snippet,statistics", id=channel_id).execute()
        else:
            resp = yt.channels().list(part="snippet,statistics", mine=True).execute()

        items = resp.get("items", [])
        if not items:
            return "Channel not found."

        ch = items[0]
        snippet = ch["snippet"]
        stats = ch["statistics"]
        subs = int(stats.get("subscriberCount", 0))
        views = int(stats.get("viewCount", 0))
        videos = int(stats.get("videoCount", 0))

        return (
            f"Channel: {snippet['title']}\n"
            f"Subscribers: {subs:,}\n"
            f"Total Views: {views:,}\n"
            f"Total Videos: {videos:,}\n"
            f"Description: {snippet.get('description', 'N/A')[:200]}"
        )
    except Exception as e:
        return f"Failed to get channel stats: {e}"


@mcp.tool()
def youtube_video_details(video_id: str) -> str:
    """Get detailed information about a YouTube video (title, description, views, likes, comments, published date)."""
    try:
        yt = get_youtube_service()
        resp = yt.videos().list(
            part="snippet,statistics", id=video_id
        ).execute()

        items = resp.get("items", [])
        if not items:
            return f"Video '{video_id}' not found."

        v = items[0]
        snippet = v["snippet"]
        stats = v.get("statistics", {})
        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))
        desc = snippet.get("description", "N/A")
        desc_preview = desc[:400] + "..." if len(desc) > 400 else desc

        return (
            f"Title: {snippet['title']}\n"
            f"Channel: {snippet['channelTitle']}\n"
            f"Published: {snippet['publishedAt']}\n"
            f"Views: {views:,}\n"
            f"Likes: {likes:,}\n"
            f"Comments: {comments:,}\n"
            f"URL: https://www.youtube.com/watch?v={video_id}\n"
            f"Description:\n{desc_preview}"
        )
    except Exception as e:
        return f"Failed to get video details: {e}"


@mcp.tool()
def youtube_my_videos(limit: int = 10) -> str:
    """List the authenticated user's uploaded YouTube videos."""
    try:
        yt = get_youtube_service()

        ch_resp = yt.channels().list(part="contentDetails", mine=True).execute()
        items = ch_resp.get("items", [])
        if not items:
            return "No channel found for the authenticated user."

        uploads_playlist = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

        pl_resp = yt.playlistItems().list(
            part="snippet", playlistId=uploads_playlist, maxResults=limit
        ).execute()

        videos = pl_resp.get("items", [])
        if not videos:
            return "No uploaded videos found."

        video_ids = [v["snippet"]["resourceId"]["videoId"] for v in videos]
        stats_resp = yt.videos().list(
            part="statistics", id=",".join(video_ids)
        ).execute()
        stats_map = {v["id"]: v.get("statistics", {}) for v in stats_resp.get("items", [])}

        results = []
        for v in videos:
            snippet = v["snippet"]
            vid = snippet["resourceId"]["videoId"]
            stats = stats_map.get(vid, {})
            views = int(stats.get("viewCount", 0))
            results.append(
                f"Title: {snippet['title']}\n"
                f"Published: {snippet['publishedAt']}\n"
                f"Views: {views:,}\n"
                f"URL: https://www.youtube.com/watch?v={vid}"
            )
        return "\n---\n".join(results)
    except Exception as e:
        return f"Failed to list your videos: {e}"


# ============================================================
# Instagram Tools
# ============================================================

@mcp.tool()
def instagram_profile() -> str:
    """Get Instagram business profile info (followers, posts count, bio) via Meta Graph API."""
    try:
        if not INSTAGRAM_BUSINESS_ID:
            return "INSTAGRAM_BUSINESS_ID env var not set."

        data = meta_get(
            INSTAGRAM_BUSINESS_ID,
            {"fields": "username,name,biography,followers_count,follows_count,media_count"},
        )
        return (
            f"Username: @{data.get('username', 'N/A')}\n"
            f"Name: {data.get('name', 'N/A')}\n"
            f"Bio: {data.get('biography', 'N/A')}\n"
            f"Followers: {data.get('followers_count', 0):,}\n"
            f"Following: {data.get('follows_count', 0):,}\n"
            f"Posts: {data.get('media_count', 0):,}"
        )
    except Exception as e:
        return f"Failed to get Instagram profile: {e}"


@mcp.tool()
def instagram_recent_posts(limit: int = 5) -> str:
    """Get recent Instagram posts with caption, likes, comments, media URL."""
    try:
        if not INSTAGRAM_BUSINESS_ID:
            return "INSTAGRAM_BUSINESS_ID env var not set."

        data = meta_get(
            f"{INSTAGRAM_BUSINESS_ID}/media",
            {"fields": "caption,like_count,comments_count,timestamp,media_url,permalink", "limit": str(limit)},
        )
        posts = data.get("data", [])
        if not posts:
            return "No recent posts found."

        results = []
        for p in posts:
            caption = p.get("caption", "No caption")
            caption_preview = caption[:200] + "..." if len(caption) > 200 else caption
            results.append(
                f"Caption: {caption_preview}\n"
                f"Likes: {p.get('like_count', 0):,}\n"
                f"Comments: {p.get('comments_count', 0):,}\n"
                f"Posted: {p.get('timestamp', 'N/A')}\n"
                f"Media: {p.get('media_url', 'N/A')}\n"
                f"Link: {p.get('permalink', 'N/A')}"
            )
        return "\n---\n".join(results)
    except Exception as e:
        return f"Failed to get Instagram posts: {e}"


@mcp.tool()
def instagram_post_insights(media_id: str) -> str:
    """Get insights (impressions, reach, engagement) for a specific Instagram post."""
    try:
        data = meta_get(
            f"{media_id}/insights",
            {"metric": "impressions,reach,engagement"},
        )
        metrics = data.get("data", [])
        if not metrics:
            return f"No insights available for media {media_id}."

        results = []
        for m in metrics:
            values = m.get("values", [{}])
            value = values[0].get("value", 0) if values else 0
            results.append(f"{m.get('title', m.get('name', 'Unknown'))}: {value:,}")

        return f"Insights for post {media_id}:\n" + "\n".join(results)
    except Exception as e:
        return f"Failed to get post insights: {e}"


# ============================================================
# Facebook Tools
# ============================================================

@mcp.tool()
def facebook_page_info() -> str:
    """Get Facebook page info (name, followers, likes, category)."""
    try:
        if not FACEBOOK_PAGE_ID:
            return "FACEBOOK_PAGE_ID env var not set."

        data = meta_get(
            FACEBOOK_PAGE_ID,
            {"fields": "name,fan_count,followers_count,about,category"},
        )
        return (
            f"Page: {data.get('name', 'N/A')}\n"
            f"Category: {data.get('category', 'N/A')}\n"
            f"Page Likes: {data.get('fan_count', 0):,}\n"
            f"Followers: {data.get('followers_count', 0):,}\n"
            f"About: {data.get('about', 'N/A')}"
        )
    except Exception as e:
        return f"Failed to get Facebook page info: {e}"


@mcp.tool()
def facebook_recent_posts(limit: int = 5) -> str:
    """Get recent Facebook page posts with message, shares, likes, and comments."""
    try:
        if not FACEBOOK_PAGE_ID:
            return "FACEBOOK_PAGE_ID env var not set."

        data = meta_get(
            f"{FACEBOOK_PAGE_ID}/posts",
            {
                "fields": "message,created_time,shares,likes.summary(true),comments.summary(true)",
                "limit": str(limit),
            },
        )
        posts = data.get("data", [])
        if not posts:
            return "No recent posts found."

        results = []
        for p in posts:
            message = p.get("message", "No message")
            msg_preview = message[:200] + "..." if len(message) > 200 else message
            shares = p.get("shares", {}).get("count", 0)
            likes = p.get("likes", {}).get("summary", {}).get("total_count", 0)
            comments = p.get("comments", {}).get("summary", {}).get("total_count", 0)
            results.append(
                f"Message: {msg_preview}\n"
                f"Posted: {p.get('created_time', 'N/A')}\n"
                f"Likes: {likes:,} | Comments: {comments:,} | Shares: {shares:,}\n"
                f"Post ID: {p.get('id', 'N/A')}"
            )
        return "\n---\n".join(results)
    except Exception as e:
        return f"Failed to get Facebook posts: {e}"


@mcp.tool()
def facebook_post_to_page(message: str) -> str:
    """Post a message to the Facebook page."""
    try:
        if not FACEBOOK_PAGE_ID:
            return "FACEBOOK_PAGE_ID env var not set."
        if not message.strip():
            return "Message cannot be empty."

        data = meta_post(f"{FACEBOOK_PAGE_ID}/feed", {"message": message})
        post_id = data.get("id", "unknown")
        return f"Successfully posted to Facebook page. Post ID: {post_id}"
    except Exception as e:
        return f"Failed to post to Facebook: {e}"


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    mcp.run(transport="stdio")
