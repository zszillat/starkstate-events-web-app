from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from datetime import timedelta
from django.core.paginator import Paginator

from .models import Event, Club, Feedback, Attendance
from .forms import CustomLoginForm, EventForm, FeedbackForm, RSVPForm

# Logs the user out and redirects to the homepage
def logout_view(request):
    logout(request)
    return redirect("/")

# Adds a new event for the logged-in user's associated club
def add_event(request):
    user = request.user

    # Try to retrieve the club associated with the user
    try:
        club = user.club
    except Club.DoesNotExist:
        club = None

    if not club:
        return render(request, 'error.html', {'message': 'You are not associated with any club.'})

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club  # Link the event to the user's club
            event.save()
            return redirect('my_events')
    else:
        form = EventForm()

    return render(request, 'add_event.html', {'form': form})

# Handles user login using CustomLoginForm
def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("/")
    else:
        form = CustomLoginForm()

    return render(request, "login.html", {"form": form, "user": request.user})

# Displays the homepage with upcoming and recent past events
def home(request):
    PER_PAGE = 5  # Events per page

    today = now().date()
    four_weeks_ago = today - timedelta(weeks=4)

    clubs = Club.objects.order_by('name')

    # Get upcoming events
    events_queryset = Event.objects.filter(date__gte=today) \
        .select_related('club') \
        .annotate(attendee_count=Count('attendance')) \
        .order_by('date')

    paginator = Paginator(events_queryset, PER_PAGE)
    page_number = request.GET.get('page')
    events_page = paginator.get_page(page_number)

    # Get recent past events (last 4 weeks)
    past_events = Event.objects.filter(date__range=[four_weeks_ago, today - timedelta(days=1)]) \
        .select_related('club') \
        .annotate(attendee_count=Count('attendance')) \
        .order_by('date')[:10]

    return render(request, 'home.html', {
        "user": request.user,
        'events': events_page,
        'past_events': past_events,
        'clubs': clubs
    })

# Lists events created by the logged-in user's clubs
def my_events(request):
    user = request.user
    clubs = Club.objects.filter(account=user)
    events = Event.objects.filter(club__in=clubs)
    return render(request, 'my_events.html', {'events': events})

# Allows club members to edit their events
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id, club__account=request.user)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('my_events')
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form, 'event': event})

# Displays a single event page with RSVP or feedback form
def event(request, event_id):
    event_obj = get_object_or_404(Event, id=event_id)
    today = now().date()

    # Show FeedbackForm for past events
    if event_obj.date < today:
        form_type = "feedback"
        if request.method == "POST" and 'feedback' in request.POST:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                student = form.cleaned_data['student']
                feedback_text = form.cleaned_data['feedback']
                feedback_obj, created = Feedback.objects.get_or_create(
                    student=student,
                    event=event_obj,
                    defaults={'feedback': feedback_text}
                )
                if created:
                    return redirect('thank_you')
                else:
                    form.add_error(None, "You’ve already submitted feedback for this event.")
        else:
            form = FeedbackForm()
    else:
        # Show RSVPForm for upcoming events
        form_type = "rsvp"
        if request.method == "POST" and 'rsvp' in request.POST:
            form = RSVPForm(request.POST)
            if form.is_valid():
                student = form.cleaned_data['student']
                attendance, created = Attendance.objects.get_or_create(student=student, event=event_obj)
                if created:
                    return redirect('thank_you')
                else:
                    form.add_error(None, "You have already RSVPed for this event.")
        else:
            form = RSVPForm()

    return render(request, 'event.html', {'event': event_obj, 'form': form, 'form_type': form_type})

# Displays a simple thank-you page
def thanks(request):
    return render(request, 'thanks.html')

# Shows details for a specific club, including upcoming events
def club(request, club_id):
    club_obj = get_object_or_404(Club, id=club_id)
    upcoming_events = Event.objects.filter(club=club_obj, date__gte=now().date()).order_by('date')
    return render(request, 'club.html', {'club': club_obj, 'upcoming_events': upcoming_events})

# Lists all past events (within 6 months) for feedback
def feedback_landing(request):
    six_months_ago = now().date() - timedelta(days=180)
    past_events = Event.objects.filter(date__gte=six_months_ago, date__lt=now().date()) \
                               .select_related('club') \
                               .order_by('-date')

    paginator = Paginator(past_events, 18)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    return render(request, 'feedback.html', {'events': events})

# Displays a list of all clubs
def clubs(request):
    clubs_list = Club.objects.order_by('name')
    return render(request, 'clubs.html', {'clubs': clubs_list})

# Deletes an event if it belongs to the logged-in user's club
@require_POST
def delete_event(request, event_id):
    event_obj = get_object_or_404(Event, pk=event_id, club__account=request.user)
    event_obj.delete()
    return redirect('my_events')
