from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def homepage(request):
    return render(request, 'home.html')

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