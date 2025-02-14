from django.utils.timezone import now
from django.db.models import Count
from .models import Event, Club
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomLoginForm, EventForm

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
            return redirect('myevents')  # Redirect to a page listing all events (change as needed)
    else:
        form = EventForm()

    return render(request, 'addevent.html', {'form': form})

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


def homepage(request):
    today = now().date()

    clubs = Club.objects.order_by('name')
    
    # Fetch events with related club data and annotate with attendee count
    events = Event.objects.filter(date__gte=today) \
        .select_related('club') \
        .annotate(attendee_count=Count('attendance')) \
        .order_by('date')

    return render(request, 'home.html', {
        "user": request.user,
        'events': events,
        'clubs': clubs
        })

def my_events(request):
    user = request.user  # Get the logged-in user
    clubs = Club.objects.filter(account=user)  # Find clubs where the user is an account holder
    events = Event.objects.filter(club__in=clubs)  # Get all events for these clubs

    return render(request, 'myevents.html', {'events': events})

def event(request):
    return render(request, 'event.html')

def account(request):
    return render(request, 'account.html')

def new(request):
    return render(request, 'new.html')

def club(request):
    return render(request, 'club.html')

def clubs(request):
    return render(request, 'clubs.html')