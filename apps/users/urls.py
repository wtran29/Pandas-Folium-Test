from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^translate$', views.translate),
    url(r'^yes$', views.yes),
    url(r'^no$', views.no),
    url(r'^map$', views.random_map)
]