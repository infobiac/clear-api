"""trustcoin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from django.contrib import admin
from django.http import HttpResponse
from api import views
import verifiee.views
import verifier.views
import seeker.views

router = routers.DefaultRouter()
router.register(r'users', views.PersonViewSet)

router.register(r'contracts', views.ContractViewSet)
router.register(r'verifier_contracts', views.VerifierContractViewSet)

urlpatterns = [
    path('', views.landing),
    path('admin/', admin.site.urls),
    # path('', lambda a : HttpResponse("Fuck off")),
    url(r'^', include(router.urls)),
    path("score/", views.score),
    path("score/pagerank/", views.prscore),
    # path("create/", views.create_new_contract),
    # path("metatest/", views.metatest),
    path("verifiee/home/", verifiee.views.home),
    path("verifiee/register/", verifiee.views.register_address),
    path("verifiee/get_from_addr/", verifiee.views.name_from_uuid),
    path("verifiee/get_from_uuid/", verifiee.views.addr_from_uuid),

    path("verifier/home/", verifier.views.home),
    path("verifier/register/", verifier.views.register_address),
    path("verifier/get_from_addr/", verifier.views.name_from_uuid),
    path("verifier/deny/", verifier.views.deny),
    path("verifier/accept/", verifier.views.accept),
    path("verifier/expose/", verifier.views.expose_data),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

    path("seeker/home/", seeker.views.home),
    path("seeker/register/", seeker.views.register_address),
    path("seeker/get_from_addr/", seeker.views.name_from_uuid),
    path("seeker/scan/", seeker.views.scanning_page),


]
