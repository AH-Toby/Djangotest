from django.conf.urls import include, url
from django.contrib import admin

from booktest import views

urlpatterns = [
    url(r'^index$', views.index),
    url(r'^testQuery$', views.testQuery),
    url(r'^testQuery1$', views.testQuery1),
    url(r'^testjoin$', views.testjoin),
    url(r'^testjoin1$', views.testjoin1),
    url(r'^testself$', views.testself),
    url(r'^showbooks$', views.showbooks),
    url(r'^createbook$', views.createbook),
    url(r'^deletebook_(\d+)$', views.deletebook),
    url(r'^testwork$', views.testwork),
]
