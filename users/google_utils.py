from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_google_calendar_service(session):
    creds_data = session.get('credentials')
    if not creds_data:
        return None

    creds = Credentials(
        token=creds_data['token'],
        refresh_token=creds_data.get('refresh_token'),
        token_uri=creds_data['token_uri'],
        client_id=creds_data['client_id'],
        client_secret=creds_data['client_secret'],
        scopes=creds_data['scopes']
    )
    return build('calendar', 'v3', credentials=creds)
