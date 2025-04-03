from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('event/<int:event_id>', views.event, name='event_details'),
    path('event/<int:event_id>/feedback', views.feedback, name='leave_feedback'),
    path('thanks', views.thanks, name="thank_you"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("myevents/", views.my_events, name="my_events"),
    path("myevents/add/", views.add_event, name="add_event"),
    path('myevents/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('new/', views.new, name='new'),
    path('club/<int:club_id>', views.club, name='club'),
    path('clubs', views.clubs, name='clubs'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
]
