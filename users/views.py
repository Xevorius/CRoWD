import datetime
from io import BytesIO

import jwt
import qrcode
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authenticators.user_authenticator import UserAuthenticator
from .mail import activateEmail, resetEmail
from .serializers import UserSerializer, ChangePasswordSerializer, ResetPasswordSerializer, NewPasswordSerializer, \
    LoginSerializer
from .token_generator import account_activation_token

User = get_user_model()


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    model = User

    def post(self, request, *args, **kwargs) -> Response:
        """
        This function is linked to the auth/register path of this API. It will take the new user data from the HTTP
        request and add it to the database.

        @param request: HTTP request object containing the data for a new user.
        @return: An echo of the data using an HTTP response to indicate the registration was successful.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['is_active'] = False
            serializer.is_valid(raise_exception=True)
            serializer.save()
            activateEmail(request, serializer.instance, serializer.data.get('email'))
            return Response({
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                })
        return Response({
                'status': 'success',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Please check if you correctly typed your email address.',
                'data': []
            })


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    model = User

    def post(self, request, *args, **kwargs) -> Response:
        """
        This function is linked to the auth/login path of this API. It will take the inputted credentials and varify
        them. If the credentials are correct, this function will return a JWT token that is valid for 1 day.

        @param request: Http containing the credentials of a user
        @return: Http response containing the JWT token as well as a cookie containing
        the same token under variable 'jwt'
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(Q(email=serializer.data.get("email"))).first()
            if not user:
                return Response({
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'User does not exist',
                })
            if not user.check_password(request.data['password']):
                return Response({
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Incorrect password',
                })
            if not user.is_active:
                return Response({
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'This account has not been activated yet. Please, check you email inbox.',
                })
            token = createJWTToken(user)
            login(request, user)
            response = Response(data={'jwt': token}, status='200')
            response.set_cookie(key='jwt', value=token, httponly=True)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    def post(request) -> Response:
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
        logout(request)
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


def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "User has been activated!")
            return redirect("login")
        messages.error(request, "User activation token expired")
        return redirect("register")
    except Exception as e:
        messages.info(request, f"Error message: {e}")
        return redirect("login")


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        payload = UserAuthenticator(request)
        user = User.objects.filter(id=payload['id']).first()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(CreateAPIView):
    serializer_class = ResetPasswordSerializer
    model = User

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(Q(email=serializer.data.get("email"))).first()
            if not user:
                return Response({"message": ["Email not found in our system."]}, status=status.HTTP_400_BAD_REQUEST)
            resetEmail(request, user, serializer.data.get("email"))
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': f'An email has been sent to {serializer.data.get("email")}',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewPasswordView(UpdateAPIView):
    serializer_class = NewPasswordSerializer
    model = User

    def update(self, request, uid64, token):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                uid = force_str(urlsafe_base64_decode(uid64))
                user = User.objects.get(pk=uid)
                if account_activation_token.check_token(user, token):
                    user.set_password(serializer.data.get("new_password"))
                    user.save()
                    messages.success(request, "Password updated successfully!")
                    response = {
                        'status': 'success',
                        'code': status.HTTP_200_OK,
                        'message': f'Your password has been reset!',
                        'data': []
                    }
                    return Response(response)
                response = {
                    'status': 'success',
                    'code': status.HTTP_406_NOT_ACCEPTABLE,
                    'message': f'Your password reset token expired.',
                    'data': []
                }
                return Response(response)
            response = {
                'status': 'success',
                'code': status.HTTP_406_NOT_ACCEPTABLE,
                'message': f'Serializer caught an error.',
                'data': []
            }
            return Response(response)
        except Exception as e:
            response = {
                'status': 'success',
                'code': status.HTTP_406_NOT_ACCEPTABLE,
                'message': f'An error occurred: {e}.',
                'data': []
            }
            return Response(response)