
from django.db import models
from django.contrib.auth.models import User

class PublicUser(models.Model):
	user = models.ForeignKey(User, unique=True)

	def __unicode__(self):
		return self.user.username
