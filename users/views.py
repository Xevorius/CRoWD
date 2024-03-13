import datetime
from io import BytesIO

import jwt
import qrcode
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from authenticators.user_authenticator import UserAuthenticator
from .serializers import UserSerializer


class RegisterView(APIView):
    @staticmethod
    def post(request) -> Response:
        """
        This function is linked to the auth/register path of this API. It will take the new user data from the HTTP
        request and add it to the database.

        @param request: HTTP request object containing the data for a new user.
        @return: An echo of the data using an HTTP response to indicate the registration was successful.
        """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    @staticmethod
    def post(request) -> Response:
        """
        This function is linked to the auth/login path of this API. It will take the inputted credentials and varify
        them. If the credentials are correct, this function will return a JWT token that is valid for 1 day.

        @param request: Http containing the credentials of a user
        @return: Http response containing the JWT token as well as a cookie containing
        the same token under variable 'jwt'
        """
        user = User.objects.filter(username=request.data['username']).first()

        if user is None:
            raise AuthenticationFailed('User does not exist!')

        if not user.check_password(request.data['password']):
            raise AuthenticationFailed('Incorrect password!')

        token = createJWTToken(user)
        response = Response(data={'jwt': token})
        response.set_cookie(key='jwt', value=token, httponly=True)
        return response


def createJWTToken(user: User) -> str:
    """
    This function will create a JWT token that is valid for 1 day based on the given user.

    @param user: User object representing the verified user.
    @return: JWT token as a string.
    """
    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }

    return jwt.encode(payload, 'secret', algorithm='HS256')


class UserView(APIView):
    @staticmethod
    def get(request) -> Response:
        """
        This function is linked to the auth/user path of this API. It will return the basic information about the
        authenticated user in a http request.

        @param request: Http request containing the JWT token as a cookie.
        @return: Http response containing some basic information about the user.
        """
        payload = UserAuthenticator(request)
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    @staticmethod
    def post() -> Response:
        """
        This function is linked to the auth/logout path of this API. This function will delete the jwt cookie from the
        http response, logging out the user.

        @return: Http response without jwt token cookie.
        """
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class UserQrView(APIView):
    @staticmethod
    def get(request) -> HttpResponse:
        """
        This function is linked to the auth/qr path of this API. This function will generate a user specific qr code
        as an image and return the bytes in a http response.

        @param request: Http request containing the JWT token as a cookie.
        @return: Http response containing the bytes for the qr code.
        """
        payload = UserAuthenticator(request)
        return createUserQrCodeFromJwtToken(UserSerializer(User.objects.filter(id=payload['id']).first()).data)


def createUserQrCodeFromJwtToken(data) -> HttpResponse:
    """
    This function will generate an image containing a QR code and then transform that image into a byte string.
    This byte string is then returned in a http response.

    @param payload: a decoded JWT token containing a users information
    @return: Http response containing the bytes for the qr code.
    """
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="White")
    byte_io = BytesIO()
    img.save(byte_io, 'png')
    byte_io.seek(0)
    return HttpResponse(byte_io, content_type="image/png")
