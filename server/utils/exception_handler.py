import logging
import re
import sys
import traceback
from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import Http404
from djangorestframework_camel_case.util import (camelize_re,
                                                 underscore_to_camel)
from rest_framework import exceptions, status
from rest_framework.views import Response
from rest_framework_simplejwt.exceptions import InvalidToken


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Custom exception handler."""

    # initialize empty error response
    error_response = {
        "error": {
            "code": "",
            "message": "",
        }
    }

    if isinstance(exc, Http404):  # Django exception
        exc = exceptions.NotFound()  # Django REST exception

    if isinstance(exc, PermissionDenied):  # Django exception
        exc = exceptions.PermissionDenied()  # Django REST exception

    # set status code, code and message only when exception is instance of APIException
    if isinstance(exc, exceptions.APIException):
        if isinstance(exc, exceptions.ValidationError):
            if isinstance(exc.detail, list):
                # take only first error from array
                message = str(exc.detail[0])
            elif isinstance(exc.detail, dict):
                # take only first error from dict
                first_error = next(iter((exc.detail.items())))
                fld_name = first_error[0]
                # camelize field name
                if "_" in fld_name:
                    fld_name = re.sub(camelize_re, underscore_to_camel, fld_name)
                fld_error = str(first_error[1])
                message = f"Field '{fld_name}' has error: {fld_error}"
            else:
                message = str(exc.detail)
            code = "invalid_request"
            status_code = status.HTTP_400_BAD_REQUEST
        elif isinstance(exc, InvalidToken):
            code = exc.detail["messages"][0]["message"].code
            message = str(exc.detail["messages"][0]["message"])
            status_code = exc.status_code
        else:
            full_detail = exc.get_full_details()
            code = full_detail["code"]
            message = full_detail["message"]
            status_code = exc.status_code

        error_response["error"]["code"] = code
        error_response["error"]["message"] = message

        response = Response(error_response, status=status_code)
    else:
        # log exception info
        type_, value, traceback_ = sys.exc_info()
        logging.error(
            f"Original error detail and callstack: {type_}\n{value}\n{''.join(traceback.format_tb(traceback_))}"
        )
        response = Response(
            {
                "error": {
                    "code": "internal_error",
                    "message": "Internal server error",
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # returns response
    return response
