from django.db import models
import datetime
from django.contrib.auth.models import User

class UserInfo(models.Model):
	user_userid = models.CharField(max_length=1000, blank=False)
	user_token = models.CharField(max_length=1000, blank=False)
	user_firstName = models.CharField(max_length=1000, blank=False)
	user_lastName = models.CharField(max_length=1000, blank=False)
	user_teamId = models.CharField(max_length=1000, blank=False)

	def __unicode__(self):
		return self.user_userid


class ExpenseInfo(models.Model):
	exp_paid = models.CharField(max_length=1000, blank=False)
	exp_for = models.CharField(max_length=1000, blank=False)
	exp_amount = models.CharField(max_length=1000, blank=False)

	def __unicode__(self):
		return self.exp_paid