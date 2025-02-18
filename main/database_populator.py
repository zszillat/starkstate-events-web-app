from faker import Faker
import os
import sys

# Set up the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "starkstate_events_web_app.settings")
import django
django.setup()

# Now the import should work
from main.models import Student

def add_random_students(num_students):
    fake = Faker()
    # Base ID: 00100000 as integer (100000)
    base_id = 100000

    # Determine the current highest ID in the Student table
    max_student = Student.objects.order_by("-id").first()
    if max_student:
        try:
            # Convert existing id to an integer and increment
            current_id = int(max_student.id) + 1
        except ValueError:
            # If conversion fails, fallback to base_id
            current_id = base_id
    else:
        current_id = base_id

    for _ in range(num_students):
        first_name = fake.first_name()
        last_name = fake.last_name()
        # Generate a birthday
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=30)
        # Format birthday month and day as MMDD
        month_day = f"{birthday.month:02d}{birthday.day:02d}"
        
        # Construct the initial email: first initial + last name + birthday (MMDD) @starkstate.net
        base_email = f"{first_name[0].lower()}{last_name.lower()}{month_day}@starkstate.net"
        
        # Check if this email already exists
        if Student.objects.filter(email=base_email).exists():
            # If email exists, append the student id instead
            email = f"{first_name[0].lower()}{last_name.lower()}{current_id:08d}@starkstate.net"
        else:
            email = base_email

        # Format the student ID as an 8-digit string with leading zeros
        student_id = f"{current_id:08d}"

        # Create and save the new student
        student = Student(
            id=student_id,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        student.save()

        current_id += 1

add_random_students(100)