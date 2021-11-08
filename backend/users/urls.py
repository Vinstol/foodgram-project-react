from django.urls import path, include
from djoser.views import  TokenCreateView, TokenDestroyView

from users.views import FollowApiView, ListFollowViewSet

urlpatterns = [
     path('', include('djoser.urls')),
     path('auth/token/login/', TokenCreateView.as_view(), name='login'),
     path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
     path('users/<int:id>/subscribe/',
          FollowApiView.as_view(),
          name='subscribe'
     ),
     path('users/subscriptions/',
          ListFollowViewSet.as_view(),
          name='subscription'
     ),
]