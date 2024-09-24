"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from decouple import config
from django.contrib import admin
from django.urls import path,reverse,include
from django.urls.conf import re_path
from allauth.account.views import ConfirmEmailView
from django.http import HttpResponsePermanentRedirect
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
from customers.views import CurrentUser

def home(request):
    return HttpResponsePermanentRedirect(reverse("swagger-ui"))

admin.site.site_header="Ecommerce API Administration"
ADMIN_SITE_URL="{}/".format(config('ADMIN_SITE_URL'))
URL_HEADER="ecommerce-api/v1"

urlpatterns = [
    path("", home, name="home"),
    path(ADMIN_SITE_URL, admin.site.urls),
    path(f"{URL_HEADER}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(f"{URL_HEADER}/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # user endpoints
    path(f"{URL_HEADER}/user/",CurrentUser.as_view(),name="current-user"),
    # account-confirm-email/
    re_path(f"{URL_HEADER}/registration/account-confirm-email/(?P<key>[-:\w]+)/$", ConfirmEmailView.as_view(),name='account_confirm_email'),
    # registration/ verify-email/ resend-email/ account-email-verification-sent/
    path(f"{URL_HEADER}/registration/",include("dj_rest_auth.registration.urls")),
    # apps endpoint
    path(f"{URL_HEADER}/users/",include("customers.urls")),
]
