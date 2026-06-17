from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Device
from .serializers import DeviceSerializer
from users.permissions import IsAdminOrEngineer


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        queryset = Device.objects.all()

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(device_type__icontains=search)

        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrEngineer()]
        return [IsAuthenticated()]
