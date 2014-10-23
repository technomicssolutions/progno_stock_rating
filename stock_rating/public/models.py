
from django.db import models
from django.contrib.auth.models import User
from web.models import Company

class PublicUser(models.Model):
	user = models.ForeignKey(User, unique=True)

	def __unicode__(self):
		return self.user.username

class WatchList(models.Model):

	user = models.ForeignKey(PublicUser)
	companies = models.ManyToManyField(Company)

	def __unicode__(self):
		return self.user.user.username


class CompareList(models.Model):

	user = models.ForeignKey(PublicUser)
	companies = models.ManyToManyField(Company)

	def __unicode__(self):
		return self.user.user.username


