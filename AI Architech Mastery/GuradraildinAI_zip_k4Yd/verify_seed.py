import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client
import config

client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_KEY)

for table in ["students", "courses", "transactions", "guardrail_logs"]:
    r = client.table(table).select("id", count="exact").execute()
    print(f"{table}: {r.count} rows")

s = client.table("students").select("first_name, last_name, major, gpa").limit(3).execute()
print("\nSample students:")
for row in s.data:
    print(f"  {row['first_name']} {row['last_name']} | {row['major']} | GPA: {row['gpa']}")

c = client.table("courses").select("course_code, course_name, department, fee").limit(3).execute()
print("\nSample courses:")
for row in c.data:
    print(f"  {row['course_code']}: {row['course_name']} | {row['department']} | ${row['fee']}")

t = client.table("transactions").select("transaction_type, amount, status, payment_method").limit(3).execute()
print("\nSample transactions:")
for row in t.data:
    print(f"  {row['transaction_type']} | ${row['amount']} | {row['status']} | {row['payment_method']}")
