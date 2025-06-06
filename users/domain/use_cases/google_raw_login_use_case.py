import os
import jwt
import hashlib
import requests

from typing import Dict
from django.conf import settings
from urllib.parse import urlencode
from django.urls import reverse_lazy

from core.utils import OrderlyAuthBaseModel
from users.exceptions import ErrorObtainingAccessToken

class GoogleAccessTokens(OrderlyAuthBaseModel):
    id_token: str
    access_token: str

    def decode_id_token(self) -> Dict[str, str]:
        decoded_token = jwt.decode(jwt=self.id_token, options={"verify_signature": False})
        return decoded_token

class GoogleTokensResponse(GoogleAccessTokens):
    refresh_token: str

# Reference: https://developers.google.com/identity/openid-connect/openid-connect#python
class GoogleRawLoginUseCase:
    def __init__(self):
        self.APP_URL = settings.APP_URL
        self.API_URI = reverse_lazy("users:google_oauth_callback")
        self.GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
        self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
        self.GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
        self.SCOPES = [ "openid", "email", "profile" ]

    @staticmethod
    def _generate_state_session_token() -> str:
        return hashlib.sha256(os.urandom(1024)).hexdigest()

    def _get_redirect_uri(self) -> str:
        return f"{self.APP_URL}{self.API_URI}"

    def get_authorization_url(self) -> tuple[str, str]:
        redirect_uri = self._get_redirect_uri()
        state = self._generate_state_session_token()
        query_params = urlencode({
            "response_type": "code",
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.SCOPES),
            "state": state,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "consent select_account",
        })
        return f"{self.GOOGLE_AUTH_URL}?{query_params}", state

    def get_tokens(self, *, code: str) -> GoogleTokensResponse:
        redirect_uri = self._get_redirect_uri()
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
        response = requests.post(self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
        if not response.ok:
            raise ErrorObtainingAccessToken
        tokens = response.json()
        return GoogleTokensResponse(
            id_token=tokens["id_token"],
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"]
        )

    def get_user_info(self, *, google_tokens: GoogleAccessTokens):
        access_token = google_tokens.access_token
        return requests.get(
            self.GOOGLE_USER_INFO_URL,
            params={"access_token": access_token}
        )

