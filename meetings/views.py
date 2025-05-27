from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import localtime, now, make_aware
from django.contrib import messages
from .models import Meeting, Attendance
from .forms import MeetingForm
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.conf import settings
import datetime

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save()

            creds_data = request.session.get('credentials')
            if creds_data:
                try:
                    creds = Credentials(
                        token=creds_data['token'],
                        refresh_token=creds_data.get('refresh_token'),
                        token_uri=creds_data['token_uri'],
                        client_id=creds_data['client_id'],
                        client_secret=creds_data['client_secret'],
                        scopes=creds_data['scopes']
                    )

                    service = build('calendar', 'v3', credentials=creds)

                    start_datetime = make_aware(datetime.datetime.combine(meeting.date, meeting.time))
                    end_datetime = start_datetime + datetime.timedelta(hours=1)

                    event = {
                        'summary': f'Meeting at {meeting.venue}',
                        'description': meeting.description,
                        'agenda' : meeting.agenda,
                        'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'Asia/Hong_Kong'},
                        'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'Asia/Hong_Kong'},
                    }

                    created_event = service.events().insert(calendarId='primary', body=event).execute()
                    meeting.google_event_id = created_event['id']
                    meeting.save()

                    messages.success(request, "Meeting created and synced with Google Calendar.")
                except Exception as e:
                    messages.warning(request, f"Meeting saved, but Google Calendar sync failed: {str(e)}")
            else:
                messages.info(request, "Meeting created, but your Google Calendar is not connected.")

            return redirect('meeting_created')
    else:
        form = MeetingForm()
    return render(request, 'meetings/create_meeting.html', {'form': form})

@login_required
def mark_attendance(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    Attendance.objects.get_or_create(user=request.user, meeting=meeting)
    return render(request, 'meetings/meeting_status.html', {
        'message': '✅ Meeting attended successfully!'
    })

@login_required
def end_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    if request.user.is_superuser:
        meeting.ended = True
        meeting.save()
    return render(request, 'meetings/meeting_status.html', {
        'message': '✅ Meeting ended successfully!'
    })


@login_required
def attendance_success(request):
    return render(request, 'meetings/meeting_success.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def end_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)

    if request.method == 'POST':
        meeting.ended = True
        meeting.save()

        creds_data = request.session.get('credentials')
        if creds_data and meeting.google_event_id:
            try:
                creds = Credentials(
                    token=creds_data['token'],
                    refresh_token=creds_data.get('refresh_token'),
                    token_uri=creds_data['token_uri'],
                    client_id=creds_data['client_id'],
                    client_secret=creds_data['client_secret'],
                    scopes=creds_data['scopes']
                )

                service = build('calendar', 'v3', credentials=creds)
                service.events().delete(calendarId='primary', eventId=meeting.google_event_id).execute()
                messages.success(request, "Meeting ended and deleted from Google Calendar.")
            except Exception as e:
                messages.warning(request, f"Meeting ended, but failed to delete from Google Calendar: {str(e)}")

        return redirect('meeting_ended')



def categorize_meetings():
    current_time = localtime(now())
    ongoing = []
    upcoming = []

    meetings = Meeting.objects.filter(ended=False)

    for meeting in meetings:
        meeting_datetime = make_aware(datetime.datetime.combine(meeting.date, meeting.time))
        if meeting_datetime <= current_time:
            ongoing.append(meeting)
        else:
            upcoming.append(meeting)

    past = Meeting.objects.filter(ended=True)
    return ongoing, upcoming, past


@login_required
def dashboard(request):
    ongoing, upcoming, _ = categorize_meetings()
    return render(request, 'users/dashboard.html', {
        'ongoing_meetings': ongoing,
        'upcoming_meetings': upcoming,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def all_meetings_view(request):
    current_time = localtime(now())

    ongoing = Meeting.objects.filter(
        ended=False,
        date=current_time.date(),
        time__lte=current_time.time()
    ).order_by('time')

    upcoming = Meeting.objects.filter(
        ended=False
    ).exclude(
        id__in=ongoing.values_list('id', flat=True)
    ).order_by('date', 'time')

    past = Meeting.objects.filter(ended=True).order_by('-date', '-time')

    return render(request, 'meetings/all_meetings.html', {
        'ongoing_meetings': ongoing,
        'upcoming_meetings': upcoming,
        'past_meetings': past,
    })

@login_required
def meeting_created(request):
    return render(request, 'meetings/meeting_status.html', {'message': 'Meeting Created Successfully ✅'})

@login_required
def meeting_ended(request):
    return render(request, 'meetings/meeting_status.html', {'message': 'Meeting Ended Successfully ✅'})
