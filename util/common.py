from rest_framework.response import Response


def send_response(response_code: int, data: dict = None, message: str = None, error: str = None):
    return Response(data=dict(
        response_code=response_code,
        message=message,
        error=error,
        data=data
    ), status=response_code)
