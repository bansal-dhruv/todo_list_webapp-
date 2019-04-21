from django.db import models
from . import managers
from django.utils import timezone
from datetime import datetime

class login(models.Model):
	username = models.CharField(max_length=30, primary_key=True)
	password = models.CharField(max_length=300)
	email = models.CharField(max_length=38)
	objects = managers.login_manager()

class schedules(models.Model):
	id = models.IntegerField(primary_key=True)
	email = models.CharField(max_length=38)
	work = models.TextField(max_length=100)
	status = models.CharField(max_length=15, default="Imcomplete")
	startdate = models.DateTimeField(default=timezone.now)
	enddate = models.DateTimeField(default=timezone.now)
	objects = managers.schedule_manager()
