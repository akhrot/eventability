from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, DateField
from datetime import datetime, timedelta, date, time
import operator

from .forms import UserForm
from .models import Building, Allotment


# Create your views here.

def homeview(request):
	today_min = datetime.combine(date.today(), time.min)
	today_max = datetime.combine(date.today(), time.max)
	allotments = Allotment.objects.filter(status=1)
	newallotments = []
	allotlength = 0
	for allotment in allotments:
		if datetime.combine(allotment.allot_date, time.max) >= today_min and datetime.combine(allotment.allot_date, time.min) <= today_max:
			newallotments.append(allotment)
			allotlength = allotlength+1

	if not request.user.is_authenticated():
		return render(request, 'events/homevisitor.html', {'slideobjects': newallotments, 'givenrange': range(1, allotlength)})

	if request.user.username=="admin":
		return render(request, 'events/homeadmin.html', {'slideobjects': newallotments, 'givenrange': range(1, allotlength)})

	return render(request, 'events/home.html', {'slideobjects': newallotments, 'givenrange': range(1, allotlength)})


def index(request):
	if not request.user.is_authenticated():
		return render(request, 'events/login.html')
	else:
		if request.user.username=="admin":
			return indexadmin(request)
		buildings = Building.objects.all()
		query = request.GET.get("q")
		if query:
			searchresults = buildings.filter(
				Q(name__icontains=query) |
				Q(desc__icontains=query)
			).distinct()
			return render(request, 'events/index.html', {
				'searchresults': searchresults,
			})
		else:
			buildings.order_by('name')
			return render(request, 'events/index.html', {'buildings': buildings})

def indexadmin(request):
	if not request.user.is_authenticated():
		return render(request, 'events/login.html')
	else:
		if request.user.username!="admin":
			return index(request)
		buildings = Building.objects.all()
		query = request.GET.get("q")
		if query:
			searchresults = buildings.filter(
				Q(name__icontains=query) |
				Q(desc__icontains=query)
			).distinct()
			return render(request, 'events/indexadmin.html', {
				'buildings': buildings,
				'searchresults': searchresults,
			})
		else:
			return render(request, 'events/indexadmin.html', {'buildings': buildings})

def login_user(request):
	print("\nlogin_user view called\n")
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		if username=="admin":
			return render(request, 'events/login.html', {'error_message': 'Admin should use the admin login'})

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return index(request)
			else:
				return render(request, 'events/login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'events/login.html', {'error_message': 'Invalid login'})
	return render(request, 'events/login.html')

def login_admin(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		if not username=="admin":
			return render(request, 'events/login.html', {'error_message2': 'Only for Admin. Users use the User login'})

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return indexadmin(request)
			else:
				return render(request, 'events/login.html', {'error_message2': 'Your account has been disabled'})
		else:
			return render(request, 'events/login.html', {'error_message2': 'Invalid login'})
	return render(request, 'events/login.html')

def access_denied(request):
	if not request.user.is_authenticated():
		return render(request, 'events/access_denied_visitor.html')
	if request.user.username=="admin":
		return render(request, 'events/access_denied_admin.html')
	else:
		return render(request, 'events/access_denied.html')

def request_allot(request, building_id):
	if not request.user.is_authenticated():
		return render(request, 'events/login.html')
	else:
		if request.user.username=="admin":
			return access_denied(request)
		startdate = request.POST['startdate']
		startdate = datetime.strptime(startdate, '%Y-%m-%d')
		enddate = request.POST['startdate']
		enddate = datetime.strptime(enddate, '%Y-%m-%d')
		event = request.POST['event']
		curbuilding = Building.objects.get(id=building_id)
		allotments = Allotment.objects.filter(building=curbuilding)
		today_min = datetime.combine(date.today(), time.min)

		if(startdate < today_min):
			return render(request, 'events/detail.html', {'allotments': allotments, 'building': curbuilding, 'error_message': "Cannot book for past time bruh"})
		if startdate > enddate:
			return render(request, 'events/detail.html', {'allotments': allotments, 'building': curbuilding, 'error_message': "Start date cannot be greater than end date"})
		alloted = False
		for allotment in allotments:
			if allotment.allot_date >= startdate.date() and allotment.allot_date <= enddate.date() and allotment.status==1:
				return render(request, 'events/detail.html', {'allotments': allotments, 'building': curbuilding, 'error_message': "Already alloted on the given date"})
			if allotment.allot_date >= startdate.date() and allotment.allot_date <= enddate.date() and allotment.status==2 and allotment.club==request.user.username:
				return render(request, 'events/detail.html', {'allotments': allotments, 'building': curbuilding, 'error_message': "You already have one request pending for this date"})
		curdate = startdate
		while curdate <= enddate:
			newallotment = Allotment()
			newallotment.building = curbuilding
			newallotment.club = request.user.username
			newallotment.allot_date = curdate
			newallotment.status = 2
			newallotment.event = event
			newallotment.save()
			curdate += timedelta(days=1)
		return render(request, 'events/detail.html', {'allotments': allotments, 'building': curbuilding, 'error_message': "Request successfull"})

def logout_user(request):
	logout(request)
	form = UserForm(request.POST or None)
	context = {
		"form": form,
	}
	return render(request, 'events/login.html', context)

# def register(request):
# 	form = UserForm(request.POST or None)
# 	print("\nregister view called\n")
# 	if form.is_valid():
# 		print("form is valid")
# 		user = form.save(commit=False)
# 		username = form.cleaned_data['username']
# 		password = form.cleaned_data['password']
# 		user.set_password(password)
# 		user.save()
# 		user = authenticate(username=username, password=password)
# 		if user is not None:
# 			if user.is_active:
# 				print('\nuser is active : logging in\n')
# 				login(request, user)
# 				return render(request, 'events/index.html')
	
# 	context = {
# 		"form": form,
# 	}
# 	print('\nreturning register.html\n')
# 	return render(request, 'events/register.html', context)


def detail(request, building_id):
	if not request.user.is_authenticated():
		return render(request, 'events/login.html')
	else:
		if request.user.username=="admin":
			return access_denied(request)
		curbuilding = Building.objects.get(id=building_id)
		allotments = Allotment.objects.filter(building=curbuilding)
		allotments = allotments.filter(status=1)
		return render(request, 'events/detail.html', {'allotments': allotments, 'building': curbuilding})

def build_req(request, building_id, error_message="", error_exists=False):
	if not request.user.is_authenticated():
		return render(request, 'events/login.html')
	else:
		if request.user.username!="admin":
			return access_denied(request)
		curbuilding = Building.objects.get(id=building_id)
		all_req = Allotment.objects.filter(building=curbuilding)
		pend_req = all_req.filter(status=2)
		acc_req = all_req.filter(status=1)

		if(error_exists):
			return render(request, 'events/build_req.html', {'pend_req': pend_req, 'acc_req': acc_req, 'building': curbuilding, 'error_message': error_message})
		else:
			return render(request, 'events/build_req.html', {'pend_req': pend_req, 'acc_req': acc_req, 'building': curbuilding})

def req_accept(request, allotment_id):
	if not request.user.is_authenticated():
		return render(request, 'events/login.html')
	else:
		if request.user.username!="admin":
			return access_denied(request)
		curallotment = Allotment.objects.get(id=allotment_id)
		curbuilding = curallotment.building
		allotments = Allotment.objects.filter(building=curbuilding)
		allotments = allotments.filter(status=1)
		for allotment in allotments:
			if curallotment.allot_date == allotment.allot_date:
				return build_req(request, curbuilding.id, "Already alloted on that date", True)
		curallotment.status=1
		curallotment.save()
		return build_req(request, curbuilding.id, "Allotment request succesfully approved", True)

def req_reject(request, allotment_id):
	if not request.user.is_authenticated():
		return render(request, 'events/login.html')
	else:
		if request.user.username!="admin":
			return access_denied(request)
		curallotment = Allotment.objects.get(id=allotment_id)
		curbuilding = curallotment.building
		curallotment.status=0
		curallotment.save()
		return build_req(request, curbuilding.id, "Allotment request succesfully rejected", True)

def req_pending(request):
	if not request.user.is_authenticated():
		return render(request, 'events/login.html')
	if request.user.username!="admin":
		return access_denied(request)
	pending_req = Allotment.objects.filter(status=2)
	return render(request, "events/req_pending.html", {'pending_req': pending_req})

def req_history(request):
	if not request.user.is_authenticated():
		return render(request, 'events/login.html')
	if request.user.username!="admin":
			return access_denied(request)
	requests = Allotment.objects.filter(status=0) | Allotment.objects.filter(status=1)
	return render(request, "events/req_history.html", {'requests': requests})

def req_status(request):
	if not request.user.is_authenticated():
		return render(request, 'events/login.html')
	if request.user.username=="admin":
			return access_denied(request)
	usern=request.user.username
	requests = Allotment.objects.filter(club=usern)
	requests = reversed(list(requests))
	return render(request, "events/req_status.html", {'requests': requests})