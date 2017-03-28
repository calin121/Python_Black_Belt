from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^info/(?P<id>\d+)$', views.info, name = 'info'),
    url(r'^create$', views.create, name = 'create'),
    url(r'^add$', views.add, name = 'add'),
    url(r'^join/(?P<id>\d+)$', views.join, name = 'join'),
    url(r'^remove/(?P<id>\d+)$', views.remove, name = 'remove'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name = 'delete'),
]



