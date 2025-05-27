from django.urls import path
from users.views import register_view, user_login, user_logout, dashboard, authorize_google, oauth2callback

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('authorize_google/', authorize_google, name='authorize_google'),
    path('oauth2callback/', oauth2callback, name='oauth2callback'),
]
