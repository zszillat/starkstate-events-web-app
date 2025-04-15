from django.utils.timezone import now
from django.db.models import Count
from .models import Event, Club, Feedback, Student, Attendance
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomLoginForm, EventForm, FeedbackForm
from datetime import timedelta
from django.views.decorators.http import require_POST

def logout_view(request):
    logout(request)
    return redirect("/")  # Redirect to login page after logout

def add_event(request):
    user = request.user

    # Get the club associated with the logged-in user
    try:
        club = user.club
    except Club.DoesNotExist:
        club = None  # If no club is found, handle accordingly

    if not club:
        return render(request, 'error.html', {'message': 'You are not associated with any club.'})

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)  # Handle image upload
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club  # Assign the event to the club
            event.save()
            return redirect('my_events')  # Redirect to a page listing all events (change as needed)
    else:
        form = EventForm()

    return render(request, 'add_event.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("/")  # Redirect to the homepage or dashboard
    else:
        form = CustomLoginForm()

    return render(request, "login.html", {
        "form": form,
        "user": request.user
        })

def home(request):
    today = now().date()
    four_weeks_ago = today - timedelta(weeks=4)

    clubs = Club.objects.order_by('name')
    
    # Fetch upcoming events (events from today onwards)
    events = Event.objects.filter(date__gte=today) \
        .select_related('club') \
        .annotate(attendee_count=Count('attendance')) \
        .order_by('date')

    # Fetch past events from the last 4 weeks excluding today
    past_events = Event.objects.filter(date__range=[four_weeks_ago, today - timedelta(days=1)]) \
        .select_related('club') \
        .annotate(attendee_count=Count('attendance')) \
        .order_by('date')[:10]  # Limit to 10 entries

    return render(request, 'home.html', {
        "user": request.user,
        'events': events,
        'past_events': past_events,
        'clubs': clubs
    })

def my_events(request):
    user = request.user  # Get the logged-in user
    clubs = Club.objects.filter(account=user)  # Find clubs where the user is an account holder
    events = Event.objects.filter(club__in=clubs)  # Get all events for these clubs

    return render(request, 'my_events.html', {'events': events})

def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id, club__account=request.user)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('my_events')  # or wherever you want to redirect
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form, 'event': event})    


from django.utils.timezone import now
from django.db.models import Count
from .models import Event, Club, Feedback, Student, Attendance
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomLoginForm, EventForm, FeedbackForm
from datetime import timedelta
from django.views.decorators.http import require_POST

# ... other view functions remain unchanged ...

def event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    today = now().date()
    # Now: if event date is before today, use FeedbackForm.
    if event.date < today:
        form_type = "feedback"
        if request.method == "POST" and 'feedback' in request.POST:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                student = form.cleaned_data['student']  # Set in the form clean() method.
                feedback_text = form.cleaned_data['feedback']
                # Create Feedback if one doesn't already exist.
                feedback_obj, created = Feedback.objects.get_or_create(
                    student=student,
                    event=event,
                    defaults={'feedback': feedback_text}
                )
                if created:
                    return redirect('thank_you')
                else:
                    form.add_error(None, "You’ve already submitted feedback for this event.")
        else:
            form = FeedbackForm()
    else:
        # If event is today or in the future, show the RSVP form.
        form_type = "rsvp"
        from django import forms
        class RSVPForm(forms.Form):
            student_id = forms.CharField(label="Student ID")
            last_name = forms.CharField(label="Last Name")

            def clean(self):
                cleaned_data = super().clean()
                student_id = cleaned_data.get('student_id')
                last_name = cleaned_data.get('last_name')
                if student_id and last_name:
                    try:
                        student = Student.objects.get(id=student_id)
                        if student.last_name.lower() != last_name.lower():
                            raise forms.ValidationError("Student ID and last name do not match.")
                        cleaned_data['student'] = student
                    except Student.DoesNotExist:
                        raise forms.ValidationError("Student ID and last name do not match.")
                return cleaned_data

        if request.method == "POST" and 'rsvp' in request.POST:
            form = RSVPForm(request.POST)
            if form.is_valid():
                student = form.cleaned_data['student']
                # Create Attendance record for the RSVP.
                attendance, created = Attendance.objects.get_or_create(student=student, event=event)
                if created:
                    return redirect('thank_you')
                else:
                    form.add_error(None, "You have already RSVPed for this event.")
        else:
            form = RSVPForm()

    return render(request, 'event.html', {'event': event, 'form': form, 'form_type': form_type})



def feedback(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']  # Set in clean() method
            feedback_text = form.cleaned_data['feedback']

            # Prevent duplicate feedback submission
            feedback_obj, created = Feedback.objects.get_or_create(
                student=student,
                event=event,
                defaults={'feedback': feedback_text}
            )
            if not created:
                form.add_error(None, "You’ve already submitted feedback for this event.")
            else:
                return redirect('thank_you')  # Customize this route as needed
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {
        'form': form,
        'event': event
    })

def thanks(request):
    return render(request, 'thanks.html')

def new(request):
    return render(request, 'new.html')

def club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    return render(request, 'club.html', {'club': club})

def clubs(request):
    clubs = Club.objects.order_by('name')
    return render(request, 'clubs.html', {'clubs' : clubs})

@require_POST
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id, club__account=request.user)
    event.delete()
    return redirect('my_events')