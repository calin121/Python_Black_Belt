from django.shortcuts import render, redirect, HttpResponse
from .models import Trip
from ..login.models import User
from django.contrib import messages
import datetime 


def index(request):
	pass

def info(request, id):
	if 'user_id' in request.session:

		context = {
			'items_list': Trip.objects.filter(id = id),
		}
		return render(request, 'travel/info.html', context)
	else:
		return redirect('users:index')

def create(request):
	if 'user_id' in request.session:
		return render(request, 'travel/add.html')
	else:
		return redirect('users:index')

def add(request):
	if 'user_id' in request.session:
		if request.method == 'POST':
			user = User.objects.get(id = request.session['user_id'])
			response_from_models = Trip.objects.add_trip(request.POST, user)

			if response_from_models['status']:
	
				return redirect('users:success')

			else:
				for error in response_from_models['trip']:
					messages.error(request, error)

					return redirect('travel:create')
	else:
		return redirect('users:index')

def join(request, id):
	if 'user_id' in request.session:
		# Add item to my travel list
		user = User.objects.get(id = request.session['user_id'])
		trip = Trip.objects.get(id = id)
		trip.all_lists.add(user)

		return redirect('users:success')
	else:
		return redirect('users:index')

def remove(request, id):
	if 'user_id' in request.session:
		# Remove item from my travel list
		user = User.objects.get(id = request.session['user_id'])
		trip = Trip.objects.get(id = id)
		trip.all_lists.remove(user)

		return redirect('users:success')
	else:
		return redirect('users:index')
def delete(request, id):
	if 'user_id' in request.session:
		# Delete the trip
		Trip.objects.get(id = id).delete()

		return redirect('users:success')
	else:
		return redirect('users:index')