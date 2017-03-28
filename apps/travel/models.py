from __future__ import unicode_literals
from django.db import models
from ..login.models import User
import datetime

# Create your models here.

class TripManager(models.Manager):

	def add_trip(self, postData, id):
		errors = []

		destination = postData['destination']
		description = postData['description']
		from_date = postData['from_date']
		to_date = postData['to_date']
		creator = id

		# run validations:
		if len(destination) < 1:
			errors.append('Destination CANNOT be blank!')
		if len(description) < 1:
			errors.append('Description CANNOT be blank!')
		if from_date == '':
			errors.append('Travel Date From field CANNOT be blank!')
		else:	
			from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
			if from_date < datetime.date.today():
					errors.append("Travel Date From field CANNOT be prior to today's date")
		if to_date == '':
			errors.append('Travel Date To field CANNOT be blank!')
		else:	
			to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
			if to_date < from_date:
					errors.append("Travel Date To field CANNOT be prior to today's date")

		# If all validations pass
		response_to_views = {}

		if not errors:
			trip = Trip.objects.create(destination = destination, description = description, from_date = from_date, to_date = to_date, creator = creator)

			trip.all_lists.add(creator)
			
			# send a response to views (trip, true)
			response_to_views['trip'] = trip
			response_to_views['status'] = True

		else:
			#send a response to views (errors, false)
			response_to_views['trip'] = errors
			response_to_views['status'] = False

		return response_to_views



class Trip(models.Model):

	destination = models.CharField(max_length = 100)
	description = models.TextField(max_length = 1000)
	from_date = models.DateField(auto_now = False)
	to_date = models.DateField(auto_now = False)
	creator = models.ForeignKey(User, related_name = "trip_creator")
	all_lists = models.ManyToManyField(User, related_name = "all_trips")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True) 

	objects = TripManager()