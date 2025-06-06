from typing import Optional
from dependency_injector.wiring import Provide

from users.domain.use_cases.google_raw_login_use_case import GoogleRawLoginUseCase
from users.presentation.types import GoogleAuthCallbackResponse


class GetGoogleTokensUseCase:
    def __init__(
        self,
        google_raw_login_use_case: GoogleRawLoginUseCase = Provide["google_raw_login_use_case"],
    ) -> None:
        self.google_raw_login_use_case = google_raw_login_use_case

    def execute(
        self,
        code: Optional[str]
    ) -> GoogleAuthCallbackResponse:
        google_tokens = self.google_raw_login_use_case.get_tokens(code=code)
        return GoogleAuthCallbackResponse(
            token_id = google_tokens.decode_id_token(),
            access_token = google_tokens.access_token,
            refresh_token = google_tokens.refresh_token,
        )
