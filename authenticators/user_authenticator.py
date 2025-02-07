import jwt
from rest_framework_simplejwt.exceptions import AuthenticationFailed


def UserAuthenticator(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed()

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed()
    return payload
