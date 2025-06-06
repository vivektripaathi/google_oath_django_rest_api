from rest_framework import status

from core.exceptions import OrderlyAuthException


class ErrorAuthenticatingUserWithGoogle(OrderlyAuthException):
    code = "OrderlyAuth_USER_0001"
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Error authenticating user with google"

class CodeOrStateNotFoundException(OrderlyAuthException):
    code = "OrderlyAuth_USER_0002"
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Code or state not found in callback request parameter"

class CSRFCheckFailedException(OrderlyAuthException):
    code = "OrderlyAuth_USER_0003"
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "CSRF check failed"

class ErrorObtainingAccessToken(OrderlyAuthException):
    code = "OrderlyAuth_USER_0003"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to obtain access token from Google"