import os
import sys
import csv
import django

# Django setup (only needed if running standalone)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "starkstate_events_web_app.settings")
django.setup()

from main.models import Attendance, Event, Student  # Replace 'main' with your app name

def load_attendance_from_csv(csv_path="dummy_data/event_attendance.csv"):
    print(f"📂 Importing attendance from {csv_path}")

    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        count = 0
        skipped = 0

        for row in reader:
            try:
                event = Event.objects.get(id=row["event_id"])
                student = Student.objects.get(id=row["student_id"])

                Attendance.objects.get_or_create(
                    student=student,
                    event=event
                )
                count += 1

            except (Event.DoesNotExist, Student.DoesNotExist):
                skipped += 1
                continue

    print(f"✅ Done! {count} attendance records added. {skipped} skipped (missing student/event).")

if __name__ == "__main__":
    load_attendance_from_csv()
