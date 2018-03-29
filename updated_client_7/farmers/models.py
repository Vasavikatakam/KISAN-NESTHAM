# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.from __future__ import unicode_literals
# Create your models here
class households(models.Model):
	id1=models.IntegerField()
	house_id=models.IntegerField()
	Name=models.CharField(max_length=40)
	lat=models.FloatField()
	lon=models.FloatField()
class UserDetails(models.Model):
	username=models.CharField(max_length=40,null=True)
	mobilenumber=models.IntegerField()
class updatedUserDetails(models.Model):
	username=models.CharField(max_length=40,null=True)
	mobilenumber=models.CharField(max_length=10,null=True)
	#yearly_income=models.FloatField()
	#Area=models.FloatField()
	#isfarm=models.BooleanField()
	
