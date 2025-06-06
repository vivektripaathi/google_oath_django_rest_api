from django.urls import path

from users.presentation.views import GoogleAutView, GoogleAuthCallbackView

urlpatterns = [
    path('google_oauth_redirect/', GoogleAutView.as_view(), name='google_oauth_redirect'),
    path('google_oauth_callback/', GoogleAuthCallbackView.as_view(), name='google_oauth_callback'),
]
