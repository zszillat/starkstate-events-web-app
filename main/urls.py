from django.contrib import admin
from django.urls import path
from . import views

# URL patterns mapping paths to views
urlpatterns = [
    path('', views.home, name='home'),  # Homepage showing events and clubs
    path('event/<int:event_id>', views.event, name='event_details'),  # Individual event detail page
    path('thanks', views.thanks, name="thank_you"),  # Thank-you page after RSVP or feedback
    path("login/", views.login_view, name="login"),  # Login page
    path("logout/", views.logout_view, name="logout"),  # Logout and redirect
    path("myevents/", views.my_events, name="my_events"),  # List of events for the logged-in user's club(s)
    path("myevents/add/", views.add_event, name="add_event"),  # Form to create a new event
    path('myevents/edit/<int:event_id>/', views.edit_event, name='edit_event'),  # Edit existing event
    path('club/<int:club_id>', views.club, name='club'),  # Club profile and its upcoming events
    path('clubs', views.clubs, name='clubs'),  # List of all clubs
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),  # Delete event
    path('feedback/', views.feedback_landing, name='feedback_landing')  # Page to access feedback forms
]
