from rest_framework import serializers
from user_management.models import User, Followers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'country_code', 'mobile_number', 'status', 'is_public']


class FollowerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    follower_name = serializers.ReadOnlyField(source='follower.username')

    class Meta:
        model = Followers
        fields = ['id', 'username', 'follower_name', 'status', 'requested_on', 'updated_on']
