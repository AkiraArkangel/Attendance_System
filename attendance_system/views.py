import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

import pathlib

GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = os.path.join(settings.BASE_DIR, 'credentials', 'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
REDIRECT_URI = 'http://localhost:8000/oauth2callback/'

def authorize_google(request):
    flow = Flow.from_client_secrets_file(
        GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent select_account'
    )
    request.session['state'] = state
    return redirect(authorization_url)
    print(f"Storing state: {state}")
    request.session['state'] = state

def oauth2callback(request):
    state = request.session.get('state')
    if not state:
        return HttpResponse("Missing OAuth state. Please try again.", status=400)

    flow = Flow.from_client_secrets_file(
        GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
        scopes=SCOPES,
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

    return HttpResponse("Google Calendar connected successfully!")
    print(f"Session state: {state}")
    print(f"Returned state: {request.GET.get('state')}")