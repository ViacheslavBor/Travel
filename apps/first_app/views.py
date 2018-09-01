from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import *
from django.contrib import messages 
import bcrypt
import re
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')





def index(request):
	return render(request, 'travel/logreg.html')

def registration(request):
	errors = []
	if len(request.POST['name']) < 2:
		errors.append("Name must be at least 2 characters")
	if len(request.POST['username']) < 2:
		errors.append("Username must be at least 2 characters")
	if len(request.POST['password']) < 2:
		errors.append("Password must be at least 2 characters")
	if request.POST['password'] != request.POST['confirm']:
		errors.append("Password and password confirmation don't match. Try again!")
	
	if errors:
		for err in errors:
			messages.error(request, err)
			print(errors)
		return redirect('/main')
	
	else:	
		
			hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(name=request.POST['name'],\
									username=request.POST['username'],\
									password = hashpw)
									
			request.session['message'] = "You are registered"
			request.session['user_id'] = user.id
			return redirect('/travels')

def login(request):
	try:
		user = User.objects.get(username = request.POST['username'])

		if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
			request.session['user_id'] = user.id
			request.session['message'] = "You are logged in"
			return redirect('/travels')
		else:
			messages.error(request, 'Username or password are incorrect')
			return redirect('/main')
	except User.DoesNotExist:
		messages.error(request, "Account doesn't exist.")
		return redirect('/main')

def logout(request):
	request.session.clear()
	return redirect('/main')

def travels(request):
	current_user = User.objects.get(id = request.session['user_id'])
	context = {
		'user': current_user,
		'other_trips': Trip.objects.exclude(user = current_user).exclude(users = current_user ),
		"joined": Trip.objects.filter(users = current_user )
	}
	return render(request, 'travel/travels.html', context)


def add(request):
	return render(request, 'travel/add_trip.html')

def upload(request):
	errors = []
	if request.POST.get('destination') == "":
		errors.append('Please enter your destination')
	if request.POST.get('description') == "":
		errors.append('Please enter description')
	if request.POST.get('start') == "":
		errors.append('Please enter start date')
	if request.POST.get('end') == "":
		errors.append('Please enter end date')

	if errors:
		for err in errors:
			messages.error(request, err)
			print(errors)
		return redirect('travels/add')

	today = datetime.today()
	start_trip = datetime.strptime(request.POST['start'], "%Y-%m-%d")
	end_trip = datetime.strptime(request.POST['end'], "%Y-%m-%d")
	if start_trip < today:
		errors.append("You can't start your trip in the PAST! Duuuh")
	if end_trip < today:
		errors.append("You can't end your trip in the PAST!")
	if start_trip > end_trip:
		errors.append("That's impossible")
		
	
	if errors:
		for err in errors:
			messages.error(request, err)
			print(errors)
		return redirect('travels/add')

	else:
		current_user = User.objects.get(id=request.session['user_id'])
		trip = Trip.objects.create(destination=request.POST['destination'],\
								 description=request.POST['description'],\
								 start=request.POST['start'],\
								 end=request.POST['end'],\
								 user=current_user)
	return redirect('/travels')

def join(request, id):
	if not 'user_id' in request.session:
		return redirect('/')
	Trip.objects.get(id=id).users.add(User.objects.get(id = request.session['user_id']))
	return redirect('/travels')

def destination(request,id):
	current_user = User.objects.get(id = request.session['user_id'])
	trip = Trip.objects.get(id=id)
	join = User.objects.filter(joins=trip)
	context = {
		"show_trip": trip,
		"all_joins": join
	}
	return render(request, 'travel/destination.html', context)


