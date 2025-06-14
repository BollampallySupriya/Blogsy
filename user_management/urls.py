from django.urls import path

from .views import UserView, FollowerView

urlpatterns = [
    path('follow', FollowerView.as_view({'get': 'list', 'post': 'create'})),
    path("", UserView.as_view({'get': 'list', 'post': 'create'})),
    path("<pk>", UserView.as_view({'get': 'retrieve', 'put': 'update'})),
]