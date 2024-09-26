from django.urls import path
from .views import AddProduct,Products,ProductDetail,ModifyProduct

urlpatterns=[
    path("add/",AddProduct.as_view(),name="add-product"),
    path("",Products.as_view(),name="products"),
    path("<str:pk>/",ProductDetail.as_view(),name="product-detail"),
    path("<str:pk>/modify",ModifyProduct.as_view(),name="modify-product"),
]