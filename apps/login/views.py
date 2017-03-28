from django.shortcuts import render, redirect, HttpResponse
from .models import User
from ..travel.models import Trip
from django.contrib import messages
# Create your views here.

def index(request):

	return render(request, 'login/index.html')

def register(request):
	# invoke the method from models and capture the response
	response_from_models = User.objects.register_user(request.POST)
	# check to see if response is true
	if response_from_models['status']:
		# save user_id in session
		request.session['user_id'] = response_from_models['user'].id
		request.session['user_name'] = response_from_models['user'].name
		request.session['user_username'] = response_from_models['user'].username
		# Successfull register message
		for confirm in response_from_models['confirm']:
			messages.error(request, confirm)
		# redirect to success page
		return redirect('users:success')
	# else
	else:
		# send the error messages to client
		for error in response_from_models['user']:
			messages.error(request, error)
		# redirect to index page
		return redirect('users:index')

def login(request):
		# invoke the method from models and capture the response
	response_from_models = User.objects.login_user(request.POST)
	# check to see if response is true
	if response_from_models['status']:
		# save user_id in session
		request.session['user_id'] = response_from_models['user'].id
		request.session['user_name'] = response_from_models['user'].name
		request.session['user_username'] = response_from_models['user'].username
		# Successfull Login message
		for confirm in response_from_models['confirm']:
			messages.error(request, confirm)
		# redirect to success page
		return redirect('users:success')
	# else
	else:
		# send the error messages to client
		for error in response_from_models['user']:
			messages.error(request, error)
		# redirect to index page
		return redirect('users:index')

def success(request):
	if 'user_id' in request.session:

		context = {
			'items_list': Trip.objects.exclude(all_lists = request.session['user_id']).order_by('from_date'),
			'my_list': Trip.objects.filter(all_lists = request.session['user_id']).order_by('from_date'),
		}

		return render(request, 'login/success.html', context)
	else:
		return redirect('users:index')
def logout(request):
	request.session.clear()
	return redirect('users:index')