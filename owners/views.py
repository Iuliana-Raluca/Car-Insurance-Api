from rest_framework.generics import CreateAPIView
from .models import Owner
from .serializers import OwnerCreateSerializer

class OwnerCreateView(CreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerCreateSerializer
