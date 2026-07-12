# stdlib
import logging

# third-party
from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        formatted_errors = []
        error_code = exc.default_code

        if isinstance(exc, exceptions.ValidationError):
            message = "Invalid Input"

            for field, errors in response.data.items():
                for error in errors:
                    error_row = {'field': field, 'issue': error}
                    formatted_errors.append(error_row)
        else:
            message =  str(response.data.get('detail')) # response return error object by default

        response.data = {
            'error' : {
                'code': error_code,
                'message': message,
                'details': formatted_errors,
            }
        }

        return response

    else:
        logger.exception(exc)
        return Response({
            'error': {
                'status_code': 500,
                'code': 'server_error',
                'message': 'An unexpected error occurred on the server.',
                'details': str(exc) # Remove str(exc) in production to avoid exposing internal logic
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
