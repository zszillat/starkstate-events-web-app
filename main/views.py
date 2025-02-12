from django.utils.timezone import now
from django.db.models import Count
from .models import Event, Club
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomLoginForm

def logout_view(request):
    logout(request)
    return redirect("/")  # Redirect to login page after logout


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