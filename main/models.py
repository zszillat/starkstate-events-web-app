from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Represents a student with a unique ID, name, and email
class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=20, unique=True)  # Manually chosen ID
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name}"

# Represents a club which is optionally linked to a user account and led by a student
class Club(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    account = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="club"
    )  # Each club optionally linked to one user account
    leader = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="club_leader"
    )  # Each club has one student leader
    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    pfp = models.ImageField(
        upload_to='club_pfps/',
        null=True,
        blank=True,
        default='defaultpfp.png'  # Default image file
    )

    def __str__(self):
        return self.name

# Represents an event hosted by a club
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    club = models.ForeignKey('Club', on_delete=models.CASCADE)  # Link to the hosting club
    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField(default="17:00:00")  # Default to 5:00 PM
    description = models.TextField()
    image = models.ImageField(
        upload_to='event_images/',
        null=True,
        blank=True,
        default='defaultevent.png'  # Default event image
    )

    def __str__(self):
        return self.name

# Represents attendance for a student at an event (many-to-many relationship)
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'event')  # Prevent duplicate RSVPs

# Represents feedback provided by a student for an event
class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    feedback = models.TextField()

    class Meta:
        unique_together = ('student', 'event')  # Prevent multiple feedbacks per student per event
