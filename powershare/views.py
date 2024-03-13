from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from authenticators.user_authenticator import UserAuthenticator
from powershare.models import PowerShareStation, PowerShareOrder
from powershare.serializers import PowerShareStationSerializer, PowerShareOrderSerializer
from users.views import createUserQrCodeFromJwtToken

User = get_user_model()


class PowerShareStationViewSet(viewsets.ModelViewSet):
    queryset = PowerShareStation.objects.all()
    serializer_class = PowerShareStationSerializer

    def list(self, request):
        try:
            UserAuthenticator(request)
            queryset = PowerShareStation.objects.all()
            serializer = PowerShareStationSerializer(queryset, many=True)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            UserAuthenticator(request)
            powerStation = self.get_object()
            serializer = self.serializer_class(powerStation)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.data)

    def create(self, request):
        try:
            UserAuthenticator(request)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.errors, status=400)

    def getQr(self, request, pk=None):
        try:
            UserAuthenticator(request)
            powerStation = self.get_object()
            serializer = self.serializer_class(powerStation)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return createUserQrCodeFromJwtToken(serializer)

# def md5Authentication(data) -> dict:
#     deviceId = data['deviceId']
#     result = hashlib.md5(deviceId.encode())
#     print(result.hexdigest())


class PowerShareOrderViewSet(viewsets.ModelViewSet):
    queryset = PowerShareOrder.objects.all()
    serializer_class = PowerShareOrderSerializer

    def list(self, request):
        try:
            user = UserAuthenticator(request)
            queryset = PowerShareOrder.objects.filter(user=user['id'])
            serializer = PowerShareOrderSerializer(queryset, many=True)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.data)

    def create(self, request):
        try:
            user = UserAuthenticator(request)
            serializer = self.serializer_class(data=request.data)
            print(request.data)
            print(request.POST)
            PowerShareOrder.objects.create(pickupStation=PowerShareStation.objects.get(pk=request.data['pickupStation'])
                                           , user=User.objects.get(pk=user['id']), pickupTime=datetime.now())
            return Response(serializer.data, status=201)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)

    def retrieve(self, request, pk=None):
        try:
            UserAuthenticator(request)
            powerStationOrder = self.get_object()
            serializer = self.serializer_class(powerStationOrder)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            UserAuthenticator(request)
            powerStationOrder = self.get_object()
            serializer = self.serializer_class(powerStationOrder, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            UserAuthenticator(request)
            powerStationOrder = self.get_object()
            powerStationOrder.delete()
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(status=204)
