"""
Seed the Supabase tables with 1000+ realistic sample records.

Usage:
    python -m database.seed
"""

import random
from datetime import date, timedelta
from faker import Faker
from database.connection import get_client

fake = Faker()
Faker.seed(42)
random.seed(42)

MAJORS = [
    "Computer Science", "Mathematics", "Physics", "Biology", "Chemistry",
    "English Literature", "History", "Economics", "Business Administration",
    "Psychology", "Mechanical Engineering", "Electrical Engineering",
    "Civil Engineering", "Data Science", "Philosophy",
]

DEPARTMENTS = [
    "Computer Science", "Mathematics", "Natural Sciences", "Humanities",
    "Business", "Engineering", "Social Sciences", "Arts",
]

SEMESTERS = ["Fall 2024", "Spring 2025", "Summer 2025", "Fall 2025", "Spring 2026"]

COURSE_PREFIXES = {
    "Computer Science": "CS",
    "Mathematics": "MATH",
    "Natural Sciences": "SCI",
    "Humanities": "HUM",
    "Business": "BUS",
    "Engineering": "ENG",
    "Social Sciences": "SOC",
    "Arts": "ART",
}

COURSE_NAMES = [
    "Introduction to Programming", "Data Structures", "Algorithms",
    "Machine Learning", "Database Systems", "Web Development",
    "Calculus I", "Calculus II", "Linear Algebra", "Statistics",
    "General Physics", "Organic Chemistry", "Cell Biology",
    "Microeconomics", "Macroeconomics", "Financial Accounting",
    "English Composition", "World History", "Philosophy 101",
    "Psychology 101", "Digital Circuits", "Thermodynamics",
    "Structural Analysis", "Software Engineering", "Computer Networks",
    "Artificial Intelligence", "Operating Systems", "Discrete Math",
    "Probability Theory", "Numerical Methods", "Data Visualization",
    "Cloud Computing", "Cybersecurity Fundamentals", "Ethics in Tech",
    "Technical Writing", "Project Management", "Entrepreneurship",
    "Marketing Fundamentals", "Human Resources Management",
    "Supply Chain Management",
]

TRANSACTION_TYPES = ["enrollment", "payment", "refund", "scholarship"]
STATUSES = ["pending", "completed", "failed", "refunded"]
PAYMENT_METHODS = ["credit_card", "debit_card", "bank_transfer", "scholarship", "cash"]


def seed_students(count: int = 400):
    print(f"Seeding {count} students...")
    client = get_client()
    batch = []
    emails_seen = set()

    for _ in range(count):
        first = fake.first_name()
        last = fake.last_name()
        email = f"{first.lower()}.{last.lower()}{random.randint(1,999)}@university.edu"
        while email in emails_seen:
            email = f"{first.lower()}.{last.lower()}{random.randint(1,9999)}@university.edu"
        emails_seen.add(email)

        dob = fake.date_of_birth(minimum_age=17, maximum_age=30)
        enrollment = fake.date_between(start_date=date(2022, 1, 1), end_date=date(2025, 12, 31))

        batch.append({
            "first_name": first,
            "last_name": last,
            "email": email,
            "date_of_birth": dob.isoformat(),
            "enrollment_date": enrollment.isoformat(),
            "major": random.choice(MAJORS),
            "gpa": round(random.uniform(1.5, 4.0), 2),
            "is_active": random.random() > 0.1,
        })

    for i in range(0, len(batch), 50):
        chunk = batch[i : i + 50]
        client.table("students").insert(chunk).execute()

    print(f"  Inserted {count} students.")
    return count


def seed_courses(count: int = 80):
    print(f"Seeding {count} courses...")
    client = get_client()
    batch = []
    codes_seen = set()

    for i in range(count):
        dept = random.choice(DEPARTMENTS)
        prefix = COURSE_PREFIXES[dept]
        code = f"{prefix}-{random.randint(100,499)}"
        while code in codes_seen:
            code = f"{prefix}-{random.randint(100,499)}"
        codes_seen.add(code)

        name = random.choice(COURSE_NAMES) if i < len(COURSE_NAMES) else f"{dept} Elective {i}"
        max_enroll = random.choice([30, 40, 50, 60, 80, 100])
        current_enroll = random.randint(0, max_enroll)

        batch.append({
            "course_code": code,
            "course_name": name,
            "department": dept,
            "credits": random.choice([1, 2, 3, 4]),
            "max_enrollment": max_enroll,
            "current_enrollment": current_enroll,
            "instructor": fake.name(),
            "semester": random.choice(SEMESTERS),
            "fee": round(random.uniform(500, 5000), 2),
            "is_active": random.random() > 0.05,
        })

    for i in range(0, len(batch), 50):
        chunk = batch[i : i + 50]
        client.table("courses").insert(chunk).execute()

    print(f"  Inserted {count} courses.")
    return count


def seed_transactions(count: int = 600):
    print(f"Seeding {count} transactions...")
    client = get_client()

    students_resp = client.table("students").select("id").execute()
    courses_resp = client.table("courses").select("id, fee").execute()

    student_ids = [s["id"] for s in students_resp.data]
    courses_data = {c["id"]: c["fee"] for c in courses_resp.data}
    course_ids = list(courses_data.keys())

    if not student_ids or not course_ids:
        print("  ERROR: Seed students and courses first.")
        return 0

    batch = []
    for _ in range(count):
        sid = random.choice(student_ids)
        cid = random.choice(course_ids)
        tx_type = random.choice(TRANSACTION_TYPES)
        base_fee = float(courses_data[cid])

        if tx_type == "enrollment":
            amount = base_fee
            status = random.choices(["completed", "pending", "failed"], weights=[70, 20, 10])[0]
        elif tx_type == "payment":
            amount = base_fee
            status = random.choices(["completed", "pending"], weights=[85, 15])[0]
        elif tx_type == "refund":
            amount = round(base_fee * random.uniform(0.5, 1.0), 2)
            status = random.choices(["completed", "refunded", "pending"], weights=[50, 30, 20])[0]
        else:  # scholarship
            amount = round(base_fee * random.uniform(0.1, 1.0), 2)
            status = "completed"

        tx_date = fake.date_time_between(start_date="-2y", end_date="now").isoformat()

        batch.append({
            "student_id": sid,
            "course_id": cid,
            "transaction_type": tx_type,
            "amount": amount,
            "status": status,
            "payment_method": random.choice(PAYMENT_METHODS),
            "transaction_date": tx_date,
            "notes": fake.sentence() if random.random() > 0.6 else None,
        })

    for i in range(0, len(batch), 50):
        chunk = batch[i : i + 50]
        client.table("transactions").insert(chunk).execute()

    print(f"  Inserted {count} transactions.")
    return count


def seed_all():
    s = seed_students(400)
    c = seed_courses(80)
    t = seed_transactions(600)
    total = s + c + t
    print(f"\nTotal records seeded: {total}")
    return total


if __name__ == "__main__":
    seed_all()
