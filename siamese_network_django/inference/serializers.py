from rest_framework import serializers
from .models import CarRimType, CarRimTypeByCategory


class CarRimTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRimType
        fields = (
            "id",
            "category",
            "getImage",
        )
        
        
class CarRimTypeByCategorySerializer(serializers.ModelSerializer):    
    class Meta:
        model = CarRimTypeByCategory
        fields = (
            "id",
            "category",
            "count",
            "image",
        )
        