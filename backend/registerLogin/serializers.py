from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'aliceBlueID')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'aliceBlueID')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(self.validated_data['username'], email=self.validated_data['email'], password=self.validated_data['password'], aliceBlueID=self.validated_data['aliceBlueID'])
        return user