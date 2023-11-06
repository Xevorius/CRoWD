from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Chat
from .serializers import ChatSerializer

@api_view(['GET'])
def getRoute(request):
    return Response('Hi :)')   


@api_view(['GET'])
def get_chats(requests): 
    chats = Chat.objects.all()
    serializer = ChatSerializer(chats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user_chats(requests, pk): 
    chats = Chat.objects.filter(users=pk)
    serializer = ChatSerializer(chats, many=True)
    return Response(serializer.data)