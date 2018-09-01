from __future__ import unicode_literals
from django.db import models

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Trip(models.Model):
	destination = models.CharField(max_length=255)
	start = models.DateField()
	end = models.DateField()
	description = models.TextField() 
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, related_name='trips')
	users = models.ManyToManyField(User, related_name='joins')



		