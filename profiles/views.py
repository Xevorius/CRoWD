from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from authenticators.user_authenticator import UserAuthenticator
from profiles.models import Profile

from profiles.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request) -> Response:
        """
        This function is linked to the auth/user path of this API. It will return the basic information about the
        authenticated user in a http request.

        @param request: Http request containing the JWT token as a cookie.
        @return: Http response containing some basic information about the user.
        """
        try:
            user = UserAuthenticator(request)
            queryset = Profile.objects.filter(user=user['id'])
            serializer = ProfileSerializer(queryset.first(), many=False)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            user = UserAuthenticator(request)
            userPorfile = Profile.objects.get(pk=user['id'])
            serializer = self.serializer_class(userPorfile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.errors, status=400)
