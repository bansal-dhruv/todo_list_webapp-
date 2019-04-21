from django.db import models

class login_manager(models.Manager):
	def save_user(self, user, pwd, email):
		u = self.create(username=user, password=pwd, email=email)
		return u

class schedule_manager(models.Manager):
	def save_schedule(self, id, work, startdate, enddate, email, status="Imcomplete"):
		u = self.create(id=id, work=work, startdate=startdate, enddate=enddate, email=email, status=status)
		return u