from __future__ import unicode_literals

from collections import OrderedDict

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.forms.utils import flatatt
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.html import format_html, format_html_join
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
from frontend.models import *


class SystemHTMLForm(forms.Form):
    html = forms.CharField(widget=forms.Textarea(attrs={'rows': '30',}))
    
class NewsHTMLForm(forms.Form):
    html = forms.CharField(widget=forms.Textarea(attrs={'rows': '30',}))

class SystemForm(forms.Form):

    name = forms.CharField(max_length=100)
    language = forms.CharField(max_length=50)
    environment = forms.CharField(max_length=50)
    command = forms.CharField(max_length=200)

class SystemEditForm(forms.ModelForm):
    choices = [(group.name,group.name) for group in Group.objects.all()]
    choices = [('','')] + choices
    allowed_groups = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=choices, required = False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '10',}))

    class Meta:
        model = System
        fields = ('name','language','environment','command','description')

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)

class EmailForm(forms.Form):
    header = forms.CharField(max_length=140)
    content = forms.CharField(widget=forms.Textarea)
            
class UploadForm(forms.Form):
    systemObjects = System.objects.all()
    languages = []
    systems = []
    environments = []
    
    for system in System.objects.all():
        languages.append((system.language,system.language))
        systems.append((system.name,system.name))
        environments.append((system.environment,system.environment))
        
    language = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=languages,)
    environment = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=environments,)
    systems = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=systems)
    metadata = forms.FileField(required=False )

class UserEditForm(forms.ModelForm):

    email = forms.EmailField(max_length=254, )
    first_name = forms.CharField( max_length=30, )
    last_name = forms.CharField( max_length=30,)
    title = forms.CharField(max_length=50)
    department = forms.CharField(max_length=50,required=False)
    organisation = forms.CharField(max_length=50,required=False)
    address1 = forms.CharField(max_length=50,required=False)
    address2 = forms.CharField(max_length=50,required=False)
    city = forms.CharField(max_length=50,required=False)
    country = forms.CharField(max_length=50,required=False)
    postcode = forms.CharField(max_length=50,required=False)
    telephone = forms.CharField(max_length=50,required=False)
    fax = forms.CharField(max_length=50,required=False)
    dob = forms.CharField(max_length=50,required=False)    

    class Meta:
        model = CustomUser
        fields = ('email','first_name','last_name','title','department','organisation','address1','address2','city','country','postcode','telephone','fax','dob')

class CustomEmailField(forms.EmailField):  
    def to_python(self, value):
        return value.lower()

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))
    email = CustomEmailField(label=_('Email'), widget = forms.EmailInput, help_text=_('Enter your email.'))

    class Meta:
        model = CustomUser
        fields = ("email",'first_name','last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user