from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^main$', views.index),
	url(r'^registration$', views.registration),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^travels$', views.travels),
	url(r'^travels/add$', views.add),
	url(r'^upload$', views.upload),
	url(r'^join/(?P<id>\d+)$', views.join),
	url(r'^travels/destination/(?P<id>\d+)$', views.destination),
]