from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('event', views.event, name='event details'),
    path('login', views.login, name='login'),
    path('account', views.account, name='account'),
    path('new', views.new, name='new'),
    path('club', views.club, name='club'),
    path('clubs', views.clubs, name='clubs'),
]
