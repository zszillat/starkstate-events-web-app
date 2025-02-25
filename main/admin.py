from django.contrib import admin
from .models import Student, Club, Event, Attendance, Feedback

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'club', 'image')

class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'pfp')

admin.site.register(Student)
admin.site.register(Club, ClubAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Attendance)
admin.site.register(Feedback)
