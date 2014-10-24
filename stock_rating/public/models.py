
from django.db import models
from django.contrib.auth.models import User
from web.models import Company

class PublicUser(models.Model):
	user = models.ForeignKey(User, unique=True)

	def __unicode__(self):
		return self.user.username

class WatchList(models.Model):

	user = models.ForeignKey(PublicUser, null=True, blank=True)
	company = models.ForeignKey(Company, null=True, blank=True)
	added_on = models.DateField('Added Date', null=True, blank=True)

	def __unicode__(self):
		return self.user.user.username


class CompareList(models.Model):

	user = models.ForeignKey(PublicUser, null=True, blank=True)
	company = models.ForeignKey(Company, null=True, blank=True)
	added_on = models.DateField('Added Date', null=True, blank=True)

	def __unicode__(self):
		return self.user.user.username

# class CompanyPriceValue(models.Model):

# 	company = models.ForeignKey(Company, null=True, blank=True)
# 	bse_price = models.FloatField('BSE Price', max_length=10, null=True, blank=True)



