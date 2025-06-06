from django.shortcuts import redirect
from rest_framework.views import APIView
from dependency_injector.wiring import Provide

from users.domain.use_cases.google_raw_login_use_case import GoogleRawLoginUseCase

class GoogleAutView(APIView):
    def get(
        self, 
        request,
        google_raw_login_use_case: GoogleRawLoginUseCase = Provide["google_raw_login_use_case"],
    ):
        authorization_url, state = google_raw_login_use_case.get_authorization_url()
        request.session["google_oauth2_state"] = state
        return redirect(authorization_url)
