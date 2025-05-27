from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm, LoginForm
from .models import Profile
from meetings.models import Meeting, Attendance
from django.utils.timezone import localtime, now
import os
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError


from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileForm

def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.username = profile_form.cleaned_data['contact_number']
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return render(request, 'users/registration_success.html')

    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def user_login(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            contact_number = form.cleaned_data['contact_number']
            password = form.cleaned_data['password']

            try:
                profile = Profile.objects.get(contact_number=contact_number)
                user = authenticate(request, username=profile.user.username, password=password)
            except Profile.DoesNotExist:
                user = authenticate(request, username=contact_number, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid contact number or password.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def dashboard(request):
    current_time = localtime(now())

    ongoing_meetings = Meeting.objects.filter(
        ended=False,
        date=current_time.date(),
        time__lte=current_time.time()
    ).order_by('time')

    upcoming_meetings = Meeting.objects.filter(
        ended=False
    ).exclude(
        id__in=ongoing_meetings.values_list('id', flat=True)
    ).order_by('date', 'time')

    profile = getattr(request.user, 'profile', None)
    full_name = (
        f"{request.user.first_name} {profile.middle_name} {request.user.last_name}"
        if profile else f"{request.user.first_name} {request.user.last_name}".strip()
    ) or request.user.username

    attended_meetings = Attendance.objects.filter(user=request.user).values_list('meeting_id', flat=True)

    context = {
        'full_name': full_name,
        'is_admin': request.user.is_staff,
        'upcoming_meetings': upcoming_meetings,
        'ongoing_meetings': ongoing_meetings,
        'attended_meetings': attended_meetings,
        'position': profile.position if profile else '',
    }
    return render(request, 'users/dashboard.html', context)



@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def authorize_google(request):
    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'credentials', 'client_secret.json'),
        scopes=['https://www.googleapis.com/auth/calendar.events'],
        redirect_uri='http://localhost:8000/oauth2callback/'
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent select_account'
    )
    request.session['state'] = state
    return redirect(authorization_url)


@login_required
def oauth2callback(request):
    try:
        state = request.session.get('state')
        if not state:
            messages.error(request, "OAuth state not found in session. Please try again.")
            return redirect('dashboard')

        flow = Flow.from_client_secrets_file(
            os.path.join(settings.BASE_DIR, 'credentials', 'client_secret.json'),
            scopes=['https://www.googleapis.com/auth/calendar.events'],
            state=state,
            redirect_uri='http://localhost:8000/oauth2callback/'
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri())

        credentials = flow.credentials
        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

        messages.success(request, 'Google Calendar has been connected successfully.')
        return redirect('dashboard')

    except MismatchingStateError:
        messages.error(request, "Security error: OAuth state mismatch. Please try again.")
        return redirect('dashboard')
