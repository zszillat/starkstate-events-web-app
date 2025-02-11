from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Count
from .models import Event, Club

def homepage(request):
    today = now().date()

    clubs = Club.objects.order_by('name')
    
    # Fetch events with related club data and annotate with attendee count
    events = Event.objects.filter(date__gte=today) \
        .select_related('club') \
        .annotate(attendee_count=Count('attendance')) \
        .order_by('date')

    return render(request, 'home.html', {
        'events': events,
        'clubs': clubs
        })


def event(request):
    return render(request, 'event.html')

def login(request):
    return render(request, 'login.html')

def account(request):
    return render(request, 'account.html')

def new(request):
    return render(request, 'new.html')

def club(request):
    return render(request, 'club.html')

def clubs(request):
    return render(request, 'clubs.html')