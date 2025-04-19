from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Student, Club, Event, Attendance, Feedback

# Resource Classes
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student

class ClubResource(resources.ModelResource):
    class Meta:
        model = Club

class EventResource(resources.ModelResource):
    class Meta:
        model = Event

class AttendanceResource(resources.ModelResource):
    class Meta:
        model = Attendance

class FeedbackResource(resources.ModelResource):
    class Meta:
        model = Feedback

# Admin Classes
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ('id', 'first_name', 'last_name', 'email')

@admin.register(Club)
class ClubAdmin(ImportExportModelAdmin):
    resource_class = ClubResource
    list_display = ('name', 'leader', 'pfp')

@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):
    resource_class = EventResource
    list_display = ('name', 'date', 'club', 'image')

@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin):
    resource_class = AttendanceResource
    list_display = ('student', 'event')

@admin.register(Feedback)
class FeedbackAdmin(ImportExportModelAdmin):
    resource_class = FeedbackResource
    list_display = ('student', 'event', 'feedback')
