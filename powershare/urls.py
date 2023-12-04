from django.urls import path
from powershare.views import PowerShareStationViewSet, PowerShareOrderViewSet

urlpatterns = [
    path('', PowerShareStationViewSet.as_view({'get': 'list'}), name='power_share_station'),
    path('<int:pk>/',
         PowerShareStationViewSet.as_view({'get': 'retrieve'})),
    path('order/', PowerShareOrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='power_share_order'),
    path('order/<int:pk>/',
         PowerShareOrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]