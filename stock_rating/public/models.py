
import binascii
import os

from jsonfield import JSONField
from django.db import models
from django.contrib.auth.models import User
from web.models import Company

class PublicUser(models.Model):
	user = models.ForeignKey(User, unique=True)
	fb_details = JSONField('FB Details', null=True, blank=True)


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

class CompanyPriceValue(models.Model):

	company = models.ForeignKey(Company, null=True, blank=True)
	bse_price = models.FloatField('BSE Price', max_length=10, null=True, blank=True)
	nse_price = models.FloatField('NSE Price', max_length=10, null=True, blank=True)

	def __unicode__(self):
		return self.company.company_name

class Help(models.Model):

	name =  models.CharField('Name', max_length=200)
	email =  models.CharField('Email', max_length=200)
	message = models.TextField('Message')

	def __unicode__(self):
		return self.name



class Token(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=40, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super(Token, self).save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __unicode__(self):
        return self.token