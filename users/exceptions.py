from rest_framework import status

from core.exceptions import OrderlyAuthException


class ErrorAuthenticatingUserWithGoogle(OrderlyAuthException):
    code = "OrderlyAuth_USER_0001"
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Error authenticating user with google"