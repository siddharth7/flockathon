from django.contrib.auth.models import User
from django.http import Http404
from django.http import HttpResponseForbidden, HttpResponseServerError
# from .models import TweetInfo
from django.shortcuts import render_to_response,get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext  
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from pyflock import FlockClient, verify_event_token
from pyflock import Message, SendAs, Attachment, Views, WidgetView, HtmlView, ImageView, Image, Download, Button, OpenWidgetAction, OpenBrowserAction, SendToAppAction
import keyy
import requests
from .models import UserInfo, ExpenseInfo

#post message to flock channel : https://api.flock.co/hooks/sendMessage/04b9d56d-0bda-4b43-baff-f79b37ecf259

@csrf_exempt
def home(request):
	if(request.method=="POST"):
		try:
			print request
			name = json.loads(request.body)['name']
			if(str(name)=='client.slashCommand'):
				print "in slash command"
				
				chat = str(json.loads(request.body)['chat'])
				userid = str(json.loads(request.body)['userId'])
				text = str(json.loads(request.body)['text'])
				user_token = UserInfo.objects.get(user_userid=userid).user_token

				if(text=='in'):
					user_info = UserInfo.objects.get(user_userid = userid)
					token = user_info.user_token
					flock_client = FlockClient(token = token, app_id=keyy.app_id)
					res = flock_client.get_user_info()
					print res['firstName']
					user_info.user_firstName = str(res['firstName'])
					user_info.user_lastName = str(res['lastName'])
					user_info.user_teamId = str(res['teamId'])
					user_info.save()
				
				elif(text.split(" ")[0]=='divide'):
					url = 'https://api.flock.co/hooks/sendMessage/04b9d56d-0bda-4b43-baff-f79b37ecf259'
					usr = UserInfo.objects.get(user_userid=userid)
					txt_array = text.split(" ")
					usr_array = txt_array[1:-2]
					paid_by = UserInfo.objects.get(user_firstName = usr_array[0][1:])
					# print paid_by.user_userid
					amount = float(txt_array[len(txt_array)-1])
					item = txt_array[len(txt_array)-2]
					# print amount
					amount =amount/float(len(usr_array))
					# print amount
					txt = usr.user_firstName + " " + usr.user_lastName+" paid "+str(amount) + " for " + item +" each for "
					for us in usr_array[1:]:
						# print us[1:]
						txt+=us[1:]+", "
						userinf = UserInfo.objects.get(user_firstName = us[1:])
						# print userinf.user_userid
						exp = ExpenseInfo(exp_paid = paid_by.user_userid, exp_for = userinf.user_userid, exp_amount = amount)
						exp.save()
					
					payload = {"text": txt}
					headers = {'content-type': 'application/json'}
					r = requests.post(url, data=json.dumps(payload), headers=headers)
					print r.json()

				elif(text.split(" ")[0]=='all'):
					url = 'https://api.flock.co/hooks/sendMessage/04b9d56d-0bda-4b43-baff-f79b37ecf259'
					usr = UserInfo.objects.get(user_userid=userid)
					paid_by = UserInfo.objects.get(user_userid = userid)
					paid_for = UserInfo.objects.all()
					# print paid_by.user_userid
					amount = float(text.split(" ")[1])
					# print amount
					amount =amount/float(len(paid_for))
					# print amount
					txt = paid_by.user_firstName + " " + paid_by.user_lastName+" paid "+str(amount) + " each for "
					for us in paid_for:
						if(us.user_userid != paid_by.user_userid):
						# print us[1:]
							txt+=us.user_firstName+", "
							exp = ExpenseInfo(exp_paid = paid_by.user_userid, exp_for = us.user_userid, exp_amount = amount)
							exp.save()
					
					payload = {"text": txt}
					headers = {'content-type': 'application/json'}
					r = requests.post(url, data=json.dumps(payload), headers=headers)
					print r.json()

				elif(text.split(" ")[0]=='outstanding'):
					# url = 'https://api.flock.co/hooks/sendMessage/04b9d56d-0bda-4b43-baff-f79b37ecf259'
					if(len(text.split())==1):
						usr = UserInfo.objects.get(user_userid=userid)
						exp = ExpenseInfo.objects.all().filter(exp_for = usr.user_userid)
						amount  = 0
						for e in exp:
							amount+=float(e.exp_amount)
						
						# payload = {"text": "your outstanding is " + str(amount)}
						# headers = {'content-type': 'application/json'}
						# r = requests.post(url, data=json.dumps(payload), headers=headers)

						url="https://api.flock.co/v1/chat.sendMessage?to="
						user_id = userid
						text="your outstanding is " + str(amount)
						token=keyy.bot_token
						url+=user_id+"&text="+text+"&token="+token
						print url
						r = requests.get(url)
						print r.json()
					else:
						usr = UserInfo.objects.get(user_userid=userid)
						exp_paid = UserInfo.objects.get(user_firstName=text.split(" ")[1][1:])
						exp = ExpenseInfo.objects.all().filter(exp_for = usr.user_userid, exp_paid = exp_paid.user_userid)
						amount  = 0
						for e in exp:
							amount+=float(e.exp_amount)
						
						# payload = {"text": "your outstanding is " + str(amount)}
						# headers = {'content-type': 'application/json'}
						# r = requests.post(url, data=json.dumps(payload), headers=headers)

						url="https://api.flock.co/v1/chat.sendMessage?to="
						user_id = userid
						text="your outstanding for " + exp_paid.user_firstName + " is " + str(amount)
						token=keyy.bot_token
						url+=user_id+"&text="+text+"&token="+token
						print url
						r = requests.get(url)
						print r.json()

			elif(str(name)=='client.pressButton'):
				print "aaa"
				userid = str(json.loads(request.body)['userId'])
				print userid
				usr = UserInfo.objects.get(user_userid=userid)
				exp = ExpenseInfo.objects.all().filter(exp_for = usr.user_userid)
				amount  = 0
				for e in exp:
					amount+=float(e.exp_amount)
				
				# payload = {"text": "your outstanding is " + str(amount)}
				# headers = {'content-type': 'application/json'}
				# r = requests.post(url, data=json.dumps(payload), headers=headers)

				url="https://api.flock.co/v1/chat.sendMessage?to="
				user_id = userid
				text="your outstanding is " + str(amount)
				token=keyy.bot_token
				url+=user_id+"&text="+text+"&token="+token
				print url
				r = requests.get(url)
				print r.json()


			elif(str(name)=='app.install'):
				print "in app install"

				userid = str(json.loads(request.body)['userId'])
				token = str(json.loads(request.body)['token'])
				print token
				userinfo = UserInfo(user_userid = userid, user_token = token)
				userinfo.save()

			elif(str(name)=='client.messageAction'):
				views = Views()
				widget = WidgetView(src="http://72a0c94d.ngrok.io/payment/",height=500)
				views.add_widget(widget)
				user_guid = str(json.loads(request.body)['userId'])
				attachment = Attachment(title="Test widget", description="http://72a0c94d.ngrok.io/payment/", views=views)
				widget_message = Message(to=user_guid, attachments = [attachment])
				user_info = UserInfo.objects.get(user_userid = user_guid)
				token = user_info.user_token
				print token
				flock_client = FlockClient(token = token, app_id=keyy.app_id)
				res = flock_client.send_chat(widget_message)
				print(res)

		except KeyError:
			HttpResponseServerError("Malformed data!")
			HttpResponse("Got json data")



		return HttpResponse("Post Ok")
	else:
		url = 'https://api.flock.co/hooks/sendMessage/e0b577a0-f117-42ad-84bb-0df09b11c674'
		payload = {"text": "Welcome Back"}
		headers = {'content-type': 'application/json'}
		r = requests.post(url, data=json.dumps(payload), headers=headers)
		print r
		return HttpResponse("Get Ok")

def payment(request):
	return render(request,'app/index.html')
