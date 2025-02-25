from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('event/', views.event, name='event_details'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("myevents/", views.my_events, name="my_events"),
    path("myevents/add/", views.add_event, name="add_event"),
    path('myevents/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('new/', views.new, name='new'),
    path('club/', views.club, name='club'),
    path('clubs/', views.clubs, name='clubs'),
]
