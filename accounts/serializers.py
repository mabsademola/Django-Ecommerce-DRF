from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import Profile
class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["id", "email", "first_name", "last_name", "password", "username"]
        


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "name", 'bio', "picture"]