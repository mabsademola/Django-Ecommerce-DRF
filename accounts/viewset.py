from rest_framework import viewsets,parsers, response,status
from .models import Profile 
from .serializers import ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (parsers.MultiPartParser,parsers.FormParser)
    
    def create(self, request, *args, **kwargs):
        name = request.data["name"]
        bio = request.data["bio"]
        picture = request.data["picture"]
        
        Profile.objects.create(name = name, bio = bio, picture=picture)
        
        
        return response.Response("Profile created successfully", status=status.HTTP_200_OK)