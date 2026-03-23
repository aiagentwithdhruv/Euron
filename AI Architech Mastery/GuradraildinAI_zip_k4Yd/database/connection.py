from supabase import create_client, Client
import config


def get_supabase_client() -> Client:
    return create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_KEY or config.SUPABASE_KEY)


_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        _client = get_supabase_client()
    return _client
