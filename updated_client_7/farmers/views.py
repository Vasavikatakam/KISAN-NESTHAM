# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from models import households,updatedUserDetails
from django.http import HttpResponse
from django.template import loader
import urllib
import simplejson
import os
from . forms import NameForm,RegForm,AdminForm
import urllib2
import cookielib
from getpass import getpass
import sys
import os
from stat import *
import numpy as np
from sklearn import datasets, linear_model
import urllib2
import simplejson
import datetime
# Create your views here.


def form(request):
    form = NameForm()
    return render(request, 'farmers/form1.html', {'form': form,'adminform':AdminForm()})
def register(request):
	form=RegForm()
	return render(request,'farmers/form2.html',{'form':form})
def prompt(request):

	if request.method == 'POST':
		form = RegForm(request.POST)
    	if form.is_valid():
        	k=request.POST.get('username')
        	m=request.POST.get('mobile_number')
        	all_details=updatedUserDetails.objects.all()
        	mn=[]
        	for item in all_details:
        		mn.append(item.mobilenumber)
        	if m not in mn:
        		l=updatedUserDetails.objects.create(username=k,mobilenumber=m)
        		l.save()
        		p="You have Successfully registered...!!!"
    		else:
    			p="Mobile number is already registered...!!"
    
	return render(request,'farmers/prompt.html',{'status':p})
def checking(request):
	import numpy as np
	from sklearn import datasets, linear_model
	import urllib2
	import simplejson
	a=[]
	b=[]
	X=[]
	Y=[]
	response = urllib2.urlopen("https://openweathermap.org/data/2.5/forecast/daily?id=1277216&appid=b1b15e88fa797225412429c1c50c122a1")
	data = simplejson.load(response)
	print len(data['list'])
	for i in range(0,14):
	        a=[]
	        Y.append(data['list'][i]['temp']['max'])
	        a.append(data['list'][i]['humidity'])
	        a.append(data['list'][i]['pressure'])
	        a.append(data['list'][i]['speed'])
	        X.append(a)


	regr = linear_model.LinearRegression()


	regr.fit(X, Y)
	a1=X[len(X)-1]
	b1=X[len(X)-2]
	x=[]
	c1=[]
	for i in range(0,len(a1)):
		x.append((a1[i]+b1[i])/2)
	c1.append(x)
	X.append(x)
	y_pred = regr.predict(c1)
	allpredY=regr.predict(X)
	allpredY=allpredY.tolist()
	request.session['temperature']=y_pred[0]
	request.session['actualy']=[]
	request.session['actualy']=Y
	count=len(Y)-1
	l=[]
	year=[]
	month=[]
	day=[]
	for i in range(0,len(Y)+1):
		l.append(datetime.datetime.now()-datetime.timedelta(days=count))
		k=(datetime.datetime.now()-datetime.timedelta(days=count))
		year.append(k.year)
		month.append(k.month-1)
		day.append(k.day)
		count=count-1
		print str(k.month-1) +"*"


	context={'actualy':Y,'predictedy':allpredY,'dates':l,'year':year,'month':month,'day':day}

	#context1={'name':'vasavi'}
	#return HttpResponse(y_pred[0])
	return render(request,'farmers/graphs.html',context)

	#print diabetes_X_train
	#print diabetes_y_train	


def graph(request):
	
	#k=datetime.now()

	l=[]
	actual_y1=request.session['actualy']
	count=len(actual_y1)
	for i in range(0,len(actual_y1)+1):
		l.append(datetime.datetime.now()-datetime.timedelta(days=count))
		count=count-1
	predicted_y1=request.session['predictedy']
	context={'actu_y':actual_y1,'pred_y':predicted_y1,'dates':l}
	return render(request,'farmers/graphs.html',context)



def sendtoall(request):
	message = request.session['temperature']
	k=updatedUserDetails.objects.all()
	l=[]
	for s in k:
		l.append(s.mobilenumber)
	#number = raw_input("Enter number: ")
	#list_num=number.split(' ')
	username = "8500917955"
	passwd = "hiranits7"

	    #message = "+".join(message.split(' '))

	 #logging into the sms site
	url ='http://site24.way2sms.com/Login1.action?'
	data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'

	 #For cookies

	cj= cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	 #Adding header details
	opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
	try:
		usock =opener.open(url, data)
	except IOError:
		print "error"
	       
	jession_id =str(cj).split('~')[1].split(' ')[0]
	print jession_id
	send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
	for i in range(0,len(l)):
		send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+l[i]+'&message='+'Temperature:'+str(message)+'degree celsius'+'&msgLen=136'
		opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
		try:
			sms_sent_page = opener.open(send_sms_url,send_sms_data)
		except IOError:
			print "error"
		print "success" 
	r='temp:'+str(message)+""+'\n'+'Successfully sent to all'	
	return HttpResponse(r)
	

def thanking(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            k=request.POST.get('house_id')   #storing house_id in session variable
            k=int(k)
            request.session['hid']=k

	link="http://10.0.3.23:8765/House/?format=json"
	fpoints_link="http://10.0.3.23:8765/farmpoints/?format=json"
	farm_link="http://10.0.3.23:8765/FarmTable/?format=json"
                                                       #loading json data coming from the web server
	f = urllib.urlopen(link)
	myfile = simplejson.load(f)  
	listi=[]
	count=0                                            # converting it into required form putting data in list in lists 
	
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['house_id'])
		listi[count+1].append(myfile[i]['lat'])
		listi[count+2].append(myfile[i]['lon'])
		listi[count+3].append(myfile[i]['area'])
		listi[count+4].append(myfile[i]['isfarm'])
		listi[count+5].append(myfile[i]['AnnualIncome'])
	l=[]
	for i in range(0,len(listi[0])):                   #extracting house data related to the entered house_id
		if listi[0][i]==k:
			l.append(listi[1][i])
			l.append(listi[2][i])
			l.append(listi[3][i])
			l.append(listi[5][i])
	#images
	image_link="http://10.0.3.23:8765/imagetable/?format=json"

	f = urllib.urlopen(image_link)                      #loading json data coming from the web server
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['house_idi'])              # converting it into required form putting data in list in lists 
	
		listi[count+1].append(myfile[i]['image'])
	imgtable=""
	for i in range(0,len((listi[0]))):
		if listi[0][i]==k:
			imgtable=imgtable+'http://10.0.3.23:8765'+listi[1][i]+','
	#---img close----		
	imgtable=imgtable.rstrip(',')
	str_imgt=imgtable.split(',')
	#videos
	image_link="http://10.0.3.23:8765/videotable/?format=json"

	f = urllib.urlopen(image_link)                         #loading json data coming from the web server   
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	for i in range(0,len(myfile[0])):                      # converting it into required form putting data in list in lists 
	
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['house_idv'])
		listi[count+1].append(myfile[i]['video'])
	vidtable=""
	for i in range(0,len((listi[0]))):
		if listi[0][i]==k:
			vidtable=vidtable+'http://10.0.3.23:8765'+listi[1][i]+','	
	vidtable=vidtable.rstrip(',')
	#----videotable-------
	#strim=str_imgt[0]
	listi=[]
	f = urllib.urlopen(farm_link)                              #loading json data coming from the web server
	myfile1= simplejson.load(f) 
	farm_list=[]
	for i in range(0,len(myfile1[0])):
		list_temp=[]                                            #processing
		listi.append(list_temp)
	for i in range(0,len(myfile1)):
		listi[count].append(myfile1[i]['farm_id'])
		listi[count+1].append(myfile1[i]['area'])
		listi[count+2].append(myfile1[i]['house_farm'])
	m=[]
	m1=[]

	for i in range(0,len(listi[0])):
		if listi[2][i]==k:
			m.append(listi[0][i])
			m1.append(listi[1][i])	
	
	listi=[]
	f = urllib.urlopen(fpoints_link)                                   #loading json data coming from the web server
	myfile2= simplejson.load(f) 
	farm_list=[]
	for i in range(0,len(myfile2[0])):
		list_temp=[]
		listi.append(list_temp)                                       #processing
	for i in range(0,len(myfile2)):
		listi[count].append(myfile2[i]['lat'])
		listi[count+1].append(myfile2[i]['lon'])
		listi[count+2].append(myfile2[i]['farm_idp'])
	n=[]
	if(len(m)!=0):

		for i in m:
			for j in range(0,len(listi[0])):
				if listi[2][j]==i:
					n.append(listi[0][j])
					n.append(listi[1][j])
	mem_link="http://10.0.3.23:8765/mem_details/?format=json"                #loading json data coming from the web server
	f = urllib.urlopen(mem_link)
	myfile3 = simplejson.load(f)  
	listi=[]
	for i in range(0,len(myfile3[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile3)):
		listi[count].append(myfile3[i]['house_idm'])
		listi[count+1].append(myfile3[i]['Name'])

	str1=""
	#str2="vas"
	o=[]
	for i in range(0,len(listi[0])):
		if listi[0][i]==k:
			str1=str1+listi[1][i]+", "
			#o.append(listi[1][i])
	#str1='\n'.join(o)
	str2=str1.rstrip()
	str2=str2.rstrip(',')

	farm_link="http://10.0.3.23:8765/farmcroptable/?format=json"                        #loading json data coming from the web server

	f = urllib.urlopen(farm_link)
	myfile = simplejson.load(f)  
	listi=[]
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['season_id'])
		listi[count+1].append(myfile[i]['crop'])
		listi[count+2].append(myfile[i]['farm_idc'])
	fa=""
	if(len(m)!=0):
		for i in m:
			for j in range(0,len(listi[0])):
				if(listi[2][j]==i):
					fa=fa+listi[1][j]+",";


	fa.rstrip(',')	
		
	well_link="http://10.0.3.23:8765/welltable/?format=json"                          #loading json data coming from the web server

	f = urllib.urlopen(well_link)
	myfile = simplejson.load(f)  
	listi=[]
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['lat'])
		listi[count+1].append(myfile[i]['lon'])
		listi[count+2].append(myfile[i]['depth'])
		listi[count+3].append(myfile[i]['farm_idw'])
	wc=[]
	
	if(len(m)!=0):
		for i in m:	
			for j in range(0,len(listi[0])):
				if listi[3][j]==i:
					wc.append(listi[0][j])
					wc.append(listi[1][j])
					wc.append(listi[2][j])
	


	context={'lst':l,'lst1':n,'lst2':str2,'farea':m1,'crop':fa,'wl':wc,'house_img':imgtable,'house_vid':vidtable}			
	#return HttpResponse(m1)
	return render(request, 'farmers/polygon1.html',context)
	
		






"""def imagere(request):
	image_link="http://10.0.3.23:8765/imagetable/?format=json"

	f = urllib.urlopen(image_link)
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['image'])
	k2=listi[0][0]
	img1="http://10.0.3.23:8765"+k2
	template=loader.get_template('farmers/thanks.html')
	context={'img':img1}
	return HttpResponse(template.render(context,request))"""
#This is for differentiating family sizes
def housegrp(request):
	link="http://10.0.3.23:8765/House/?format=json"
	#loading json data
	f = urllib.urlopen(link)
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	#processing
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['house_id'])
		listi[count+1].append(myfile[i]['lat'])
		listi[count+2].append(myfile[i]['lon'])

	
	link="http://10.0.3.23:8765/mem_details/?format=json"

	f = urllib.urlopen(link)
	myfile = simplejson.load(f)  
	listi2=[]
	
	
	#retrieving family size using mem_details table
	for i in range(0,len(myfile)):
		listi2.append(myfile[i]['house_idm'])
	count1=[]
	for i in range(0,len(listi[0])+1):
		count1.append(0)	
	for i in range(0,len(listi2)):
		count1[listi2[i]]=count1[listi2[i]]+1	
	for i in range(0,len(listi[0])):
		listi[count+3].append(count1[i+1])
	context={'totlst':listi}
    #template=loader.get_template('farmers/house_point.html')
  	return render(request,'farmers/familysize.html',context)
def piechart(request):
	farm_link="http://10.0.3.23:8765/farmcroptable/?format=json"

	f = urllib.urlopen(farm_link)
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	
	for i in range(0,len(myfile)):    #retrieving crops and their count          
		
		listi.append(myfile[i]['crop'])
	
	dict1={}                           #storing crop and their count in a dictionary
	for i in listi:
		if i not in dict1.keys():
			dict1[i]=1
		else:
			dict1[i]=dict1[i]+1

	context={'list':dict1}		
	  	
	return render(request,'farmers/piechart.html',context)
def welldepth(request):
	well_link="http://10.0.3.23:8765/welltable/?format=json"

	f = urllib.urlopen(well_link)
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	for i in range(0,len(myfile[0])):         #processing

		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):

		listi[count].append(myfile[i]['lat'])
		listi[count+1].append(myfile[i]['lon'])
		listi[count+2].append(myfile[i]['depth'])         #storing lat,lon,depth of a well
		listi[count+3].append(myfile[i]['well_id'])
	#---------wellyield------
	well_link="http://10.0.3.23:8765/wellinfo/?format=json"

	f = urllib.urlopen(well_link)
	myfile = simplejson.load(f)  
	listi2=[]
	count=0
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi2.append(list_temp)
	for i in range(0,len(myfile)):
		listi2[count].append(myfile[i]['well_idf'])        #storing yield of a well
		listi2[count+1].append(myfile[i]['yield1'])
		
	context={'list1':listi,'list2':listi2}
	#------------------close---------
	return render(request,'farmers/Upd_wellDepths.html',context)	



	
def wellyield(request):
	well_link="http://10.0.3.23:8765/wellinfo/?format=json"

	f = urllib.urlopen(well_link)
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['well_idf'])     #taking well yield 
		listi[count+1].append(myfile[i]['yield1'])
		
	context={'list1':listi}
	return render(request,'farmers/welldepth.html',context)	
	
def first(request):
	listi=[]
	context={'list1':listi}
	return render(request,'farmers/nav.html',context)   #mainpage


def piemap(request):
	k=request.session['hid']
	#context={'list1':listi}
	#return render(request,'farmers/nav.html',context)


	link="http://10.0.3.23:8765/House/?format=json"
	fpoints_link="http://10.0.3.23:8765/farmpoints/?format=json"
	farm_link="http://10.0.3.23:8765/FarmTable/?format=json"

	f = urllib.urlopen(link)
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['house_id'])
		listi[count+1].append(myfile[i]['lat'])
		listi[count+2].append(myfile[i]['lon'])
		listi[count+3].append(myfile[i]['area'])
		listi[count+4].append(myfile[i]['isfarm'])
		listi[count+5].append(myfile[i]['AnnualIncome'])
	l=[]
	for i in range(0,len(listi[0])):
		if listi[0][i]==k:
			l.append(listi[1][i])
			l.append(listi[2][i])
			l.append(listi[3][i])
			l.append(listi[5][i])
	#images
	image_link="http://10.0.3.23:8765/imagetable/?format=json"

	f = urllib.urlopen(image_link)
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['house_idi'])
		listi[count+1].append(myfile[i]['image'])
	imgtable=""
	for i in range(0,len((listi[0]))):
		if listi[0][i]==k:
			imgtable=imgtable+'http://10.0.3.23:8765'+listi[1][i]+','
	#---img close----		
	imgtable=imgtable.rstrip(',')
	str_imgt=imgtable.split(',')
	#videos
	image_link="http://10.0.3.23:8765/videotable/?format=json"

	f = urllib.urlopen(image_link)
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['house_idv'])
		listi[count+1].append(myfile[i]['video'])
	vidtable=""
	for i in range(0,len((listi[0]))):
		if listi[0][i]==k:
			vidtable=vidtable+'http://10.0.3.23:8765'+listi[1][i]+','	
	vidtable=vidtable.rstrip(',')
	#----videotable-------
	#strim=str_imgt[0]
	listi=[]
	f = urllib.urlopen(farm_link)
	myfile1= simplejson.load(f) 
	farm_list=[]
	for i in range(0,len(myfile1[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile1)):
		listi[count].append(myfile1[i]['farm_id'])
		listi[count+1].append(myfile1[i]['area'])
		listi[count+2].append(myfile1[i]['house_farm'])
	m=[]
	m1=[]

	for i in range(0,len(listi[0])):
		if listi[2][i]==k:
			m.append(listi[0][i])
			m1.append(listi[1][i])	
	
	listi=[]
	f = urllib.urlopen(fpoints_link)
	myfile2= simplejson.load(f) 
	farm_list=[]
	for i in range(0,len(myfile2[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile2)):
		listi[count].append(myfile2[i]['lat'])
		listi[count+1].append(myfile2[i]['lon'])
		listi[count+2].append(myfile2[i]['farm_idp'])
	n=[]
	if(len(m)!=0):

		for i in m:
			for j in range(0,len(listi[0])):
				if listi[2][j]==i:
					n.append(listi[0][j])
					n.append(listi[1][j])
	mem_link="http://10.0.3.23:8765/mem_details/?format=json"
	f = urllib.urlopen(mem_link)
	myfile3 = simplejson.load(f)  
	listi=[]
	for i in range(0,len(myfile3[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile3)):
		listi[count].append(myfile3[i]['house_idm'])
		listi[count+1].append(myfile3[i]['Name'])

	str1=""
	#str2="vas"
	o=[]
	for i in range(0,len(listi[0])):
		if listi[0][i]==k:
			str1=str1+listi[1][i]+", "
			#o.append(listi[1][i])
	#str1='\n'.join(o)
	str2=str1.rstrip()
	str2=str2.rstrip(',')

	farm_link="http://10.0.3.23:8765/farmcroptable/?format=json"

	f = urllib.urlopen(farm_link)
	myfile = simplejson.load(f)  
	listi=[]
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['season_id'])
		listi[count+1].append(myfile[i]['crop'])
		listi[count+2].append(myfile[i]['farm_idc'])
		#listi[count+3].append(myfile[i]['area'])
	fa=""
	if(len(m)!=0):
		for i in m:
			for j in range(0,len(listi[0])):
				if(listi[2][j]==i):
					fa=fa+listi[1][j]+",";


	fa.rstrip(',')	
		
	well_link="http://10.0.3.23:8765/welltable/?format=json"

	f = urllib.urlopen(well_link)
	myfile = simplejson.load(f)  
	listi=[]
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['lat'])
		listi[count+1].append(myfile[i]['lon'])
		listi[count+2].append(myfile[i]['depth'])
		listi[count+3].append(myfile[i]['farm_idw'])
	wc=[]
	
	if(len(m)!=0):
		for i in m:	
			for j in range(0,len(listi[0])):
				if listi[3][j]==i:
					wc.append(listi[0][j])
					wc.append(listi[1][j])
					wc.append(listi[2][j])
	farm_link="http://10.0.3.23:8765/newfarmcroptable/?format=json"

	f = urllib.urlopen(farm_link)
	myfile = simplejson.load(f)  
	listi=[]
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		
		listi[count].append(myfile[i]['crop'])
		listi[count+1].append(myfile[i]['farm_idnc'])
		listi[count+2].append(myfile[i]['area'])				
	flist=[]
	strc=""
	for i in range(0,len(listi[0])):      #storing farm_id,crop,area in string
		for j in m:
			if(listi[1][i]==j):
				strc=strc+str(j)+','+listi[0][i]+','+str(listi[2][i])+'*'
	strc=strc.strip('*')
				
	


	context={'lst':l,'lst1':n,'lst2':str2,'farea':m1,'crop':fa,'wl':wc,'house_img':imgtable,'house_vid':vidtable,'ncrop':strc,}			
	#return HttpResponse(m1)
	return render(request, 'farmers/piemap1.html',context)

def wateryield(request):
	well_link="http://10.0.3.23:8765/welltable/?format=json"

	f = urllib.urlopen(well_link)
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):

		listi[count].append(myfile[i]['lat'])
		listi[count+1].append(myfile[i]['lon'])
		listi[count+2].append(myfile[i]['depth'])
		listi[count+3].append(myfile[i]['well_id'])
	#---------wellyield------
	well_link="http://10.0.3.23:8765/wellinfo/?format=json"

	f = urllib.urlopen(well_link)
	myfile = simplejson.load(f)  
	listi2=[]
	count=0
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi2.append(list_temp)
	for i in range(0,len(myfile)):
		listi2[count].append(myfile[i]['well_idf'])
		listi2[count+1].append(myfile[i]['yield1'])
		
	context={'list1':listi,'list2':listi2}
	#------------------close---------
	return render(request,'farmers/Upd_wellYields.html',context)	
def annualincome(request):
	link="http://10.0.3.23:8765/House/?format=json"
	
	f = urllib.urlopen(link)
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count+0].append(myfile[i]['house_id'])         #storing annualincome
		listi[count+1].append(myfile[i]['lat'])
		listi[count+2].append(myfile[i]['lon'])
		listi[count+3].append(myfile[i]['AnnualIncome'])

	context={'list1':listi}
	return render(request,'farmers/annualincome.html',context)

def AllHouses(request):
	link="http://10.0.3.23:8765/House/?format=json"
	#loading json data
	f = urllib.urlopen(link)
	myfile = simplejson.load(f)  
	listi=[]
	count=0
	#processing
	for i in range(0,len(myfile[0])):
		list_temp=[]
		listi.append(list_temp)
	for i in range(0,len(myfile)):
		listi[count].append(myfile[i]['house_id'])
		listi[count+1].append(myfile[i]['lat'])
		listi[count+2].append(myfile[i]['lon'])

	
	link="http://10.0.3.23:8765/mem_details/?format=json"
	mem_details={}
	f = urllib.urlopen(link)
	myfile = simplejson.load(f)  
	mem_list=[]
	count=0
	#processing
	for i in range(0,len(myfile[0])):
		mem_list_temp=[]
		mem_list.append(mem_list_temp)
	for i in range(0,len(myfile)):
		mem_list[count].append(myfile[i]['house_idm'])
		mem_list[count+1].append(myfile[i]['Name'])
	uniq_list=[]	
	for i in range(0,len(mem_list[0])):
		if mem_list[0][i] not in mem_details.keys():
			mem_details[mem_list[0][i]]=[]
		mem_details[mem_list[0][i]].append(mem_list[1][i])

	members=""	
	for j in mem_details.keys():
		str1=""
		for s in mem_details[j]:
			str1=str1+s+','
		str1=str1.rstrip(',')
		members=members+str1+'*'
	members=members.rstrip('*')	
	context={'house':listi,'mem_details':members}
	return render(request,'farmers/allhouses.html',context)

def adminform(request):
	context={'form':AdminForm()}
	return render(request,'farmers/login.html',context)
def aftrlogin(request):
	if request.method == 'POST':
		form = AdminForm(request.POST)
		if form.is_valid():
			k=request.POST.get('admin_username')
    		m=request.POST.get('admin_password')
    		if k=='saikiran' and m=='saikiran123':
    			p="ok"
    		else:
    			p="not ok"
	context={'status':p}
	return render(request,'farmers/aftrlogin.html',context)

def button(request):
	context={}
	return render(request,'farmers/index.html',context)
