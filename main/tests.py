from django.test import TestCase

# Create your tests here.
for i in range(100):
    # Format the student id to have leading zeros for a total of 7 characters
    student_id = f"{base_id + i:07d}"
    
    # Generate simple first and last names (e.g. Student1, Test1)
    first_name = f"Student{i + 1}"
    last_name = f"Test{i + 1}"
    
    # Generate a random birthday (month and day)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Using 28 to avoid invalid dates
    birthday_str = f"{month:02d}{day:02d}"
    
    # Build the email: first initial, full last name, birthday, and domain.
    email = f"{first_name[0].lower()}{last_name.lower()}{birthday_str}@starkstate.net"
    
    # Create the Student record
    Student.objects.create(
        id=student_id,
        first_name=first_name,
        last_name=last_name,
        email=email
    )

def test_students_created(self):
    # Assert that 100 students were added.
    self.assertEqual(Student.objects.count(), 100)
