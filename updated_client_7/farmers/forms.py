from django import forms
from django.template.defaultfilters import mark_safe
#from phonenumber_field.formfields import PhoneNumberField

class NameForm(forms.Form):
    house_id= forms.IntegerField(label = mark_safe('<strong>HouseId</strong>'))
class RegForm(forms.Form):
	username=forms.CharField(label=mark_safe('<strong>Username  </strong>'),max_length=20)
	mobile_number=forms.CharField(label=mark_safe('<strong>MobileNumber</strong>'),max_length=10)
class AdminForm(forms.Form):
	admin_username=forms.CharField(label = mark_safe('<strong>Username</strong>'),max_length=20)
	admin_password=forms.CharField(label = mark_safe('<strong>Password</strong>'),max_length=11,widget=forms.PasswordInput)

