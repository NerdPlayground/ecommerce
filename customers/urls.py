from django.urls import path
from .views import UserList,UserDetail

urlpatterns=[
    path("",UserList.as_view(),name="user-list"),
    path("<str:username>/",UserDetail.as_view(),name="user-detail"),
]