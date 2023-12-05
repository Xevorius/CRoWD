from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from chat.views import authCheck
from powershare.models import PowerShareStation, PowerShareOrder
from powershare.serializers import PowerShareStationSerializer, PowerShareOrderSerializer


class PowerShareStationViewSet(viewsets.ModelViewSet):
    queryset = PowerShareStation.objects.all()
    serializer_class = PowerShareStationSerializer

    def list(self, request):
        try:
            authCheck(request)
            queryset = PowerShareStation.objects.all()
            serializer = PowerShareStationSerializer(queryset, many=True)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            authCheck(request)
            powerStation = self.get_object()
            serializer = self.serializer_class(powerStation)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.data)


class PowerShareOrderViewSet(viewsets.ModelViewSet):
    queryset = PowerShareOrder.objects.all()
    serializer_class = PowerShareOrderSerializer

    def list(self, request):
        try:
            user = authCheck(request)
            queryset = PowerShareOrder.objects.filter(users=user['id'])
            serializer = PowerShareOrderSerializer(queryset, many=True)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.data)

    def create(self, request):
        try:
            authCheck(request)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        try:
            authCheck(request)
            powerStationOrder = self.get_object()
            serializer = self.serializer_class(powerStationOrder)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            authCheck(request)
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
            authCheck(request)
            powerStationOrder = self.get_object()
            powerStationOrder.delete()
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(status=204)
