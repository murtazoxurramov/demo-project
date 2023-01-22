from rest_framework import generics, permissions

from .serializers import SignUpSerializer
from .models import User

class CreateUserView(generics.CreateAPIView):
    model = User
    permission_classes = (permissions.AllowAny, )
    serializer_class = SignUpSerializer
    
