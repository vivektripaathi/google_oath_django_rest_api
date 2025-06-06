from rest_framework import status
from rest_framework.exceptions import APIException


class OrderlyAuthAPIException(APIException):
    pass


class OrderlyAuthException(OrderlyAuthAPIException):
    """
    Base class for OrderlyAuth's REST framework exceptions.
    Subclasses should provide `.status_code`, `.code`  and `.default_detail` properties.
    """

    code = "OrderlyAuth_ERROR_00000"
