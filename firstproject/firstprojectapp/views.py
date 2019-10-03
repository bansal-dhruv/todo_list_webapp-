from datetime import datetime
from django.conf import settings
from django.contrib.auth.forms import *
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.template import RequestContext
from . import models
import datetime
from django.utils import timezone

inc = 0
session = {
	'logged_in': 0,
	'username': "",
	'email':""
}

def index(request):
	mail()
	global inc
	global session
	session = {
		'logged_in' : 0,
		'username' : "",
		'email':""
	}
	inc = 0
	z = models.schedules.objects.all()
	for i in z:
		inc = max(inc, i.id)
	return render(request,'home.html',{'session':session})


def mail():
	now=timezone.now()
	now=str(now)
	year=now[0:4]
	month=now[5:7]
	yearmonth=now[0:7]
	day=now[8:10]
	minutes=(int(now[11:13]))*60 + int(now[14:16])
	minutes1=(int(now[8:10]))*24*60 + (int(now[11:13]))*60 + int(now[14:16])
	z=models.schedules.objects.all()
	for i in z:
		sendmail=False
		if(str(i.status)=="Complete") :
			continue
		endtime=(str(i.enddate))
		email=str(i.email)
		if ( int(year)>int(endtime[0:4])  or ( int(year)==int(endtime[0:4]) and int(month)>int(endtime[5:7]) ) or ( int(year)==int(endtime[0:4]) and int(month)== int(endtime[5:7]) and int(day) > int(endtime[8:10]) ) ):
			sendmail=True
		if (yearmonth+'-'+day == endtime[0:10] and  abs( int(minutes) - ((int(endtime[11:13]))*60 + int(endtime[14:16])) )<=600):
			sendmail=True
		if ( (year)==(endtime[0:4]) and (month)== (endtime[5:7])  and  abs(minutes1 - ( (int(endtime[8:10]))*24*60 + (int(endtime[11:13]))*60 + int(endtime[14:16]) ) )<=600  ):
			sendmail=True
		if sendmail==True:
			k=models.login.objects.all()
			for j in k:
				if(str(j.email) == email):
					name=str(j.username)
					break
			print("Mail Sent !! ",str(i.email),settings.EMAIL_HOST_USER )
			subject = "Reminder for non-completion of your work : " + str(i.work)
			message = " <-- Do not reply below this line --> \n"
			message = message + "Hi "+name + ",\nYou haven't completed a schedule from " + str(i.startdate) + " to " + str(i.enddate) + "."
			message = message + "\nYou have forgotten to complete your "+str(i.work) + " which you have to complete by "+ endtime[0:10] + " till "+ endtime[11:16]
			message = message + "\n\n\nRegards Todo scheduler Team\n"
			recipient = [ email , settings.EMAIL_HOST_USER ,"dhruvbansal13999@gmail.com"]
			sender = settings.EMAIL_HOST_USER
			send_mail(subject, message, sender, recipient, fail_silently=True)

def login(request):
	if request.method == 'POST':
		username_cand = request.POST.get("username")
		password_cand = request.POST.get("password")
		z = models.login.objects.all()
		for i in z:
			if (username_cand == str(i.username) and password_cand ==str(i.password) ):
				session['email'] = i.email
				session['logged_in'] = 1
				session['username'] = username_cand
				return dashboard(request)
		return render(request, "register.html", {'error':'Register first!!!'})
	if request.method == 'GET':
		return render(request, "login.html", {'session':session})

def register(request):
	if request.method == 'POST':
		password = str(request.POST.get("password"))
		comfirmpassword = str(request.POST.get("confirmpassword"))
		email = request.POST.get("email")
		username = str(request.POST.get("username"))
		if password == comfirmpassword:
			try:
				User_cand = models.login.objects.save_user(username, password, email)
				User_cand.save()
			except:
				data = {
					'data1':{
						'email':"",
						'username':""
					},
					'session':{
						'logged_in' : 0,
						'username' : "",
						'email':""
					},
					'msg':'Username already exists!!'
				}
				return render(request, "register.html", data)
			z1 = models.schedules.objects.filter(email=session['email'])
			data = {
				"data1":z1,
				"session":{
					'logged_in' : 1,
					'username' : username,
					'email':email
				}
			}
			session['email'] = email
			session['logged_in'] = 1
			session['username'] = username
			return render(request, "dashboard.html", data)
		else:
			data = {
				'data1':{
					'email':email,
					'username':username
				},
				'session':{
					'logged_in' : 0,
					'username' : "",
					'email':""
				},
				'msg':"Password don't not match"
			}
			return render(request, "register.html", data)
	else:
		data = {
			'email':"",
			'username':"",
			'session':{
					'logged_in' : 0,
					'username' : "",
					'email':""
				}
		}
		return render(request, "register.html", data)

def dashboard(request):
	print(session['email'])
	z1 = models.schedules.objects.filter(email=session['email'])
	data = {
		"data1":z1,
		"session":session
	}
	return render(request, "dashboard.html", data)

def delete(request, id):
	record = models.schedules.objects.get(id=id)
	record.delete()
	z1 = models.schedules.objects.filter(email=session['email'])
	data = {
		"data1":z1,
		"session":session
	}
	return render(request, "dashboard.html", data)

def edit(request, id):
	z1 = models.schedules.objects.get(id=id)
	data = {
		"data1":z1,
		"session":session
	}
	if request.method == 'POST':
		record = models.schedules.objects.get(id=id)
		status = record.status
		record.delete()
		work = request.POST.get("work")
		startdate = request.POST.get("startdate")
		enddate = request.POST.get("enddate")
		email = session['email']
		work = work[3:len(work)-4]
		record=models.schedules.objects.save_schedule(id, work, startdate, enddate, email, status)
		record.save()
		z1 = models.schedules.objects.filter(email=session['email'])
		data = {
			"data1":z1,
			"session":session
		}
		return render(request, "dashboard.html", data)
	return render(request, "edit_schedule.html", data)

def add(request):
	print('add')
	if request.method == 'POST':
		work=request.POST.get("work")
		startdate=request.POST.get("startdate")
		enddate=request.POST.get("enddate")
		starttime=request.POST.get("starttime")
		endtime=request.POST.get("endtime")
		email=session['email']
		startdate = startdate + " " + starttime + ":27"
		enddate = enddate + " " + endtime  + ":27"
		work = work[3:len(work)-4]
		subject = "Successfully! Added a schedule."
		message = " ### Do not reply below this line ### \nHello " + session['username']
		message = message + "\nYou added a schedule from " + startdate + " to " + enddate + "."
		message = message + "\n\n\nRegards Todo scheduler Team\n"
		
		recipient = [email, settings.EMAIL_HOST_USER]
		
		sender = settings.EMAIL_HOST_USER
		
		send_mail(subject, message, sender, recipient, fail_silently=True)
		global inc
		inc = inc + 1
		record=models.schedules.objects.save_schedule(inc, work, startdate, enddate, email)
		record.save()
		z1 = models.schedules.objects.filter(email=session['email'])
		data = {
			"data1":z1,
			"session":session
		}
		return render(request, "dashboard.html", data)
	if request.method == 'GET':
		return render(request, "add_schedule.html", {'session':session})

def change(request, id):
	record = models.schedules.objects.get(id=id)
	work = record.work
	startdate = record.startdate
	enddate = record.enddate
	email = session['email']
	if record.status == "Imcomplete":
		status = "Complete"
	else:
		status = "Imcomplete"
	record.delete()
	record=models.schedules.objects.save_schedule(id, work, startdate, enddate, email, status)
	record.save()
	z1 = models.schedules.objects.filter(email=session['email'])
	data = {
		"data1":z1,
		"session":session
	}
	return render(request, "dashboard.html", data)

def logout(request):
	session = {
		'logged_in' : 0,
		'username' : ""
	}
	return render(request, "home.html", {'session':session})
