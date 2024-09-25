from django.urls import path
from .views import Orders,OrderDetail,OrdersList,Deliver

urlpatterns=[
    path("",OrdersList.as_view(),name="orders"),
    path("all/",Orders.as_view(),name="all-orders"),
    path("<str:pk>/",OrderDetail.as_view(),name="orders-detail"),
    path("<str:pk>/deliver/",Deliver.as_view(),name="deliver"),
]