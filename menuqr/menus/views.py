from rest_framework import viewsets
from .serializer import *
from .models import *

# Create your views here.
class MenuView(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
