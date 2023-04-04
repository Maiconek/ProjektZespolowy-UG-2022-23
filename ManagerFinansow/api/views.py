from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProfileSerializer
from UsersApp.models import Profile

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {"GET": '/api/profiles'}
    ]

    return Response(routes)

@api_view(['GET'])
def getProfiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)

    return Response(serializer.data)
