from typing import Optional
from core.utils import OrderlyAuthBaseModel


class GoogleAuthCallbackRequest(OrderlyAuthBaseModel):
    code: Optional[str] = None
    error: Optional[str] = None
    state: Optional[str] = None

class GoogleAuthCallbackResponse(OrderlyAuthBaseModel):
    token_id: dict
    access_token: str
    refresh_token: str
