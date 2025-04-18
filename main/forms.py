from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Event, Student

# Custom login form that validates user credentials
class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # Authenticate the user
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data

# Model form for creating or editing an event
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'description', 'image']  # Fields included in the form
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

# Form to collect and validate feedback from students
class FeedbackForm(forms.Form):
    student_id = forms.CharField(label="Student ID")
    last_name = forms.CharField(label="Last Name")
    feedback = forms.CharField(widget=forms.Textarea, label="Feedback")

    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get('student_id')
        last_name = cleaned_data.get('last_name')

        # Validate student identity
        if student_id and last_name:
            try:
                student = Student.objects.get(id=student_id)
                if student.last_name.lower() != last_name.lower():
                    raise forms.ValidationError("Student ID and last name do not match.")
                cleaned_data['student'] = student
            except Student.DoesNotExist:
                raise forms.ValidationError("Student ID and last name do not match.")
        return cleaned_data

# RSVP form used to mark attendance for upcoming events
class RSVPForm(forms.Form):
    student_id = forms.CharField(label="Student ID")
    last_name = forms.CharField(label="Last Name")

    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get('student_id')
        last_name = cleaned_data.get('last_name')

        # Validate student identity
        if student_id and last_name:
            try:
                student = Student.objects.get(id=student_id)
                if student.last_name.lower() != last_name.lower():
                    raise forms.ValidationError("Student ID and last name do not match.")
                cleaned_data['student'] = student
            except Student.DoesNotExist:
                raise forms.ValidationError("Student ID and last name do not match.")
        return cleaned_data
