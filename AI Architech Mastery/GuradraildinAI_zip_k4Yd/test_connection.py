"""Quick test: verify Supabase connection works."""
import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv()

import config
from supabase import create_client

print(f"Supabase URL: {config.SUPABASE_URL}")
print(f"Supabase Key: {config.SUPABASE_KEY[:20]}...")
print(f"Service Key:  {config.SUPABASE_SERVICE_KEY[:20]}...")
print()

try:
    client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_KEY)
    print("Client created successfully.")

    # Try a simple query to verify connectivity
    result = client.table("students").select("id").limit(1).execute()
    print(f"Query test: OK (returned {len(result.data)} rows — table may be empty if not yet created/seeded)")
    print("\nConnection test PASSED.")
except Exception as e:
    print(f"Connection test FAILED: {e}")
    sys.exit(1)
