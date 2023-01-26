from rest_framework import generics, permissions, views

from .serializers import SignUpSerializer
from .models import User

class CreateUserView(generics.CreateAPIView):
    model = User
    permission_classes = (permissions.AllowAny, )
    serializer_class = SignUpSerializer
    
    
class VerifyApiView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    
