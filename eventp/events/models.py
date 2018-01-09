from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.

#class Club(model.Model):
#	name = model.CharField(max_length=250)

class Building(models.Model):
	name = models.CharField(max_length=250)
	capacity = models.IntegerField()
	desc = models.CharField(max_length=1000)
	build_img = models.FileField()

	def __str__(self):
		return self.name

class Allotment(models.Model):
	allot_date = models.DateField()
	building = models.ForeignKey(Building, on_delete=models.CASCADE)
	club = models.CharField(max_length=250)
	status = models.IntegerField()
	event = models.CharField(max_length=250)
	
	def __str__(self):
		return str(self.allot_date) + " | " + str(self.building) + " | " + str(self.club) + " | " + str(self.event)