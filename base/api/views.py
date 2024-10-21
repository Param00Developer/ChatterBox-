from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Room
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist


from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms=Room.objects.all()
    for room in rooms:print(model_to_dict(room))
    serializeData=RoomSerializer(rooms,many=True)
    return  Response(serializeData.data)

@api_view(['GET'])
def getRoom(request,pk):
    try: 
        rooms=Room.objects.get(id=pk)
        serializeData=RoomSerializer(rooms,many=False)
        return  Response(serializeData.data)
    except ObjectDoesNotExist:
        return Response({
            'detail':'Room not found',
        })
    
