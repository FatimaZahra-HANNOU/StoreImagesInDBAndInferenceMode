from rest_framework import serializers
from .models import CarRimType


class CarRimTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRimType
        fields = (
            "id",
            "category",
            "getImage",
        )
        