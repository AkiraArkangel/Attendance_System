from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_meeting, name='create_meeting'),
    path('attendance-success/', views.attendance_success, name='attendance_success'),
    path('mark-attendance/<int:meeting_id>/', views.mark_attendance, name='mark_attendance'),
    path('all-meetings/', views.all_meetings_view, name='all_meetings'),
    path('end-meeting/<int:meeting_id>/', views.end_meeting, name='end_meeting'),
    path('created/', views.meeting_created, name='meeting_created'),
    path('ended/', views.meeting_ended, name='meeting_ended'),
]
