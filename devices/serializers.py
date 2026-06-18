from rest_framework import serializers
from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializer base para a validação dos dados de entrada e saída do modelo Device.
    Responsável por converter as instâncias do banco de dados em JSON e vice-versa.
    """
    class Meta:
        model = Device
        fields = ['id', 'name', 'device_type', 'status', 'location', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
