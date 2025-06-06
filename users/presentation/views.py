from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dependency_injector.wiring import Provide

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
    def get(
        self,
        request,
        google_raw_login_use_case: GoogleRawLoginUseCase = Provide["google_raw_login_use_case"],
    ):
        request_data = GoogleAuthCallbackRequest.parse_obj(request.GET.dict())

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

        google_tokens = google_raw_login_use_case.get_tokens(code=request_data.code)

        response = GoogleAuthCallbackResponse(
            token_id = google_tokens.decode_id_token(),
            user_info = google_raw_login_use_case.get_user_info(google_tokens=google_tokens),
            access_token = google_tokens.access_token,
            refresh_token = google_tokens.refresh_token,
        )
        return Response(response.dict_serialized(), status=status.HTTP_200_OK)
