from rest_framework import serializers
from .models import Offerings


class OfferingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offerings
        fields = '__all__'
