from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from .models import User, Followers
from .serializers import UserSerializer, FollowerSerializer
from .services.follower_management import FollowerManagementService

# Create your views here.
class UserView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class FollowerView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    serializer_class = FollowerSerializer
    
    def get_queryset(self):
        user = 1 # self.request.user
        return Followers.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        query_params = request.GET 
        type = query_params.get('type', 'followers')
        if type == 'followers':
            data = FollowerManagementService.list_followers(1)
        else:
            data = FollowerManagementService.list_following(1)
        return Response(data, status=HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        follower_id = data.get('follower_id') # request.user.id
        _status, msg = FollowerManagementService.send_follow_request(user_id=data.get('user_id'), follower_id=follower_id)
        if _status:
            return Response(msg, status=HTTP_201_CREATED)
        else:
            return Response(msg, status=HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)