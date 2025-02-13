from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=20, unique=True)  # Manually chosen ID
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name}"


class Club(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, related_name="led_clubs")
    leader = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, default=None, related_name="led_clubs")
    name = models.CharField(max_length=255)  # Changed from club_name to name
    description = models.TextField(default="", blank=True)  # Default blank description
    pfp = models.ImageField(upload_to='club_pfps/', null=True, blank=True)  # Profile Picture Field

    def __str__(self):
        return self.name


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField(default="17:00:00")  # Default time set to 5:00 PM
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)  # New ImageField

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'event')

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    feedback = models.TextField()

    class Meta:
        unique_together = ('student', 'event')
