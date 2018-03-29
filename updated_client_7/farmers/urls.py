from django.conf.urls import url
from django.contrib import admin
from . import views
app_name = 'farmers'
urlpatterns=[
#url(r'^ins',views.insert,name='insert'),
#url(r'^farm',views.farm,name='farm'),
#url(r'^house',views.house,name='house'),
url(r'^form',views.form,name='form'),  
url(r'^sms',views.register,name='sms'),         
url(r'^thanks',views.thanking,name='thanking'),
url(r'^pro',views.prompt,name='prompt'),
#url(r'^img',views.imagere,name='imagere'),
url(r'^familysize',views.housegrp,name='housegrp'),
url(r'^piechart',views.piechart,name='piechart'),
url(r'^welldepth',views.welldepth,name='welldepth'),
url(r'^piemap',views.piemap,name='piemap'),
url(r'^nav',views.first,name='first'),              #this is the main page function
url(r'^wateryield',views.wateryield,name='wateryield'),
url(r'^annualincome',views.annualincome,name='annualincome'),
url(r'^sendtoall',views.sendtoall,name='sendtoall'), 
url(r'^graph',views.graph,name='graph'),
url(r'^checking',views.checking,name='checking'),
url(r'^allhouses',views.AllHouses,name='allhouses'),
url(r'^admin',views.adminform,name='adminform'),
url(r'^aftrlogin',views.aftrlogin,name='aftrlogin'),
url(r'^index',views.button,name='button'),


#url(r'^retri',views.retrieve,name='retrieve'),
]