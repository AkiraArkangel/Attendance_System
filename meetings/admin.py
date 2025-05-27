from django.contrib import admin
from .models import Meeting, Attendance

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'venue', 'ended','agenda')
    list_filter = ('ended', 'date')
    search_fields = ('title', 'venue')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'meeting', 'timestamp')
    list_filter = ('meeting', 'timestamp')
    search_fields = ('user__first_name', 'user__last_name', 'meeting__title')
