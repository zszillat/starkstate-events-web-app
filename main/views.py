from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from datetime import timedelta
from django.core.paginator import Paginator

from .models import Event, Club, Feedback, Attendance
from .forms import CustomLoginForm, EventForm, FeedbackForm, RSVPForm


def logout_view(request):
    logout(request)
    return redirect("/")  # Redirect to homepage after logout


def add_event(request):
    user = request.user

    # Get the club associated with the logged-in user
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
            event.club = club  # Assign event to the club
            event.save()
            return redirect('my_events')
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
                return redirect("/")  # Redirect to homepage or dashboard
    else:
        form = CustomLoginForm()

    return render(request, "login.html", {"form": form, "user": request.user})


def home(request):

    #Number of events to show per page
    PER_PAGE = 5

    today = now().date()
    four_weeks_ago = today - timedelta(weeks=4)

    clubs = Club.objects.order_by('name')
    
    # Fetch upcoming events (from today onwards)
    events_queryset = Event.objects.filter(date__gte=today) \
        .select_related('club') \
        .annotate(attendee_count=Count('attendance')) \
        .order_by('date')
    
    # Paginate the upcoming events with 10 events per page
    paginator = Paginator(events_queryset, 5)
    page_number = request.GET.get('page')
    events_page = paginator.get_page(page_number)

    # Fetch past events from the last 4 weeks (excluding today)
    past_events = Event.objects.filter(date__range=[four_weeks_ago, today - timedelta(days=1)]) \
        .select_related('club') \
        .annotate(attendee_count=Count('attendance')) \
        .order_by('date')[:10]  # Limit to 10 entries

    return render(request, 'home.html', {
        "user": request.user,
        'events': events_page,  # Use the paginated results
        'past_events': past_events,
        'clubs': clubs
    })


def my_events(request):
    user = request.user
    clubs = Club.objects.filter(account=user)
    events = Event.objects.filter(club__in=clubs)
    return render(request, 'my_events.html', {'events': events})


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


def event(request, event_id):
    event_obj = get_object_or_404(Event, id=event_id)
    today = now().date()

    # Determine form type based on event date
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


def feedback(request, event_id):
    event_obj = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            feedback_text = form.cleaned_data['feedback']
            feedback_obj, created = Feedback.objects.get_or_create(
                student=student,
                event=event_obj,
                defaults={'feedback': feedback_text}
            )
            if not created:
                form.add_error(None, "You’ve already submitted feedback for this event.")
            else:
                return redirect('thank_you')
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form, 'event': event_obj})


def thanks(request):
    return render(request, 'thanks.html')


def new(request):
    return render(request, 'new.html')


def club(request, club_id):
    club_obj = get_object_or_404(Club, id=club_id)
    return render(request, 'club.html', {'club': club_obj})


def clubs(request):
    clubs_list = Club.objects.order_by('name')
    return render(request, 'clubs.html', {'clubs': clubs_list})


@require_POST
def delete_event(request, event_id):
    event_obj = get_object_or_404(Event, pk=event_id, club__account=request.user)
    event_obj.delete()
    return redirect('my_events')
