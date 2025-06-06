from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dependency_injector.wiring import Provide

from users.domain.use_cases.get_google_tokens_use_case import GetGoogleTokensUseCase
from users.domain.use_cases.google_raw_login_use_case import GoogleRawLoginUseCase
from users.exceptions import CSRFCheckFailedException, CodeOrStateNotFoundException, ErrorAuthenticatingUserWithGoogle
from users.presentation.types import GoogleAuthCallbackRequest, GoogleAuthCallbackResponse

class GoogleAutView(APIView):
    def get(
        self, 
        request,
        google_raw_login_use_case: GoogleRawLoginUseCase = Provide["google_raw_login_use_case"],
    ):
        authorization_url, state = google_raw_login_use_case.get_authorization_url()
        request.session["google_oauth2_state"] = state
        return redirect(authorization_url)


class GoogleAuthCallbackView(APIView):
    def _validate_request_and_state(
        self,
        request,
        request_data: GoogleAuthCallbackRequest
    ):
        if request_data.error is not None:
            raise ErrorAuthenticatingUserWithGoogle

        if request_data.code is None or request_data.state is None:
            raise CodeOrStateNotFoundException

        session_state = request.session.get("google_oauth2_state")

        if session_state is None:
            raise CSRFCheckFailedException

        del request.session["google_oauth2_state"]

        if request_data.state != session_state:
            raise CSRFCheckFailedException

    def get(
        self,
        request,
        get_google_tokens_use_case: GetGoogleTokensUseCase = Provide["get_google_tokens_use_case"],
    ):
        request_data = GoogleAuthCallbackRequest.parse_obj(request.GET.dict())
        self._validate_request_and_state(request, request_data)

        google_tokens = get_google_tokens_use_case.execute(code=request_data.code)

        return Response(google_tokens.dict_serialized(), status=status.HTTP_200_OK)
