from django.shortcuts import render, redirect
from . import forms
from django import forms as djangoforms
from . import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import auth
from django.utils.crypto import get_random_string
from . import mail
from django.utils import http
from django.urls import reverse
import datetime

# Create your views here.

def login_view(request):
    if request.method == 'GET':
        username = request.session.get('username')
        if username == None:
            form = forms.UserLogin()
            return render(request, 'accounts/login.html', {'form': form})
        else:
            return redirect('person:practice')
    else:
        form = forms.UserLogin(request.POST)
        if form.is_valid():
            curr_user = models.user.objects.filter(username=form.cleaned_data['username'])
            curr_user = curr_user[0]
            request.session['username'] = curr_user.username
            request.session['type'] = curr_user.user_type
            return redirect('person:practice')
        else:
            err = form.errors.as_data()
            err = err['__all__']
            return render(request, 'accounts/login.html', {'form': form, 'err': err})

def signup_view(request):
    if request.method == 'GET':
        form = forms.UserCreate()
        return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = forms.UserCreate(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            print(form.cleaned_data)
            new_user.activated = False
            token = get_random_string(length=8)
            new_user.user_token = make_password(token)
            new_user.password = make_password(form.cleaned_data['password1'])
            new_user.save()
            form.save_m2m()
            mail.sendUserRegisteredMail(new_user.username, new_user.email, token)
            return render(request, 'accounts/signup.html', {'form': forms.UserCreate(), 'success': 'Your account has been created. Please check your email for further instructions.'})
        else:
            err = form.errors
            return render(request, 'accounts/signup.html', {'form': form, 'err': err})

def activate_view(request):
    if request.method == 'GET':
        try:
            match = models.user.objects.filter(email = http.urlunquote_plus(request.GET['id']), activated = False)
        except:
            return render(request, 'not_found.html')
        if len(match) == 0:
            return render(request, 'not_found.html')
        else:
            curr_user = match[0]
            print(request.GET['token'])
            print(check_password(request.GET['token'], curr_user.user_token))
            if check_password(http.urlunquote_plus(request.GET['token']), curr_user.user_token) == True:
                curr_user.activated = True
                curr_user.save()
                return render(request, 'accounts/activate.html')
            else:
                return render(request, 'not_found.html')

def forgot_view(request):
    if request.method == 'GET':
        form = forms.UserForgot()
        return render(request, 'accounts/forgot.html', {'form': form})
    else:
        form = forms.UserForgot(request.POST)
        if form.is_valid():
            match = models.user.objects.filter(email = request.POST['email'])
            curr_user = match[0]
            token = get_random_string(length=8)
            curr_user.user_token = make_password(token)
            curr_user.save()
            mail.sendUserForgotMail(curr_user.username, curr_user.email, token)
            return render(request, 'accounts/forgot.html', {'form': form, 'success': 'Your credentials have been mailed to the registered email address.'})
        else:
            err = form.errors.as_data()
            err = err['email']
            print(err)
            return render(request, 'accounts/forgot.html', {'form': form, 'err': err})

def reset_view(request):
    if request.method == 'GET':
        try:
            match = models.user.objects.filter(email=http.urlunquote_plus(request.GET['id']))
        except:
            return render(request, 'not_found.html')
        if len(match) == 0:
            return render(request, 'not_found.html')
        else:
            curr_user = match[0]
            if check_password(http.urlunquote_plus(request.GET['token']) ,curr_user.user_token) == True:
                form = forms.UserReset()
                return render(request, 'accounts/reset.html', {'form': form, 'email': http.urlquote_plus(request.GET['id'])})
            else:
                return render(request, 'not_found.html')
    else:
        form = forms.UserReset(request.POST)
        if form.is_valid():
            match = models.user.objects.filter(email = request.GET['id'])
            curr_user = match[0]
            curr_user.password = make_password(form.cleaned_data['password1'])
            curr_user.save()
            curr_user.user_token = make_password(get_random_string(length=8))
            return render(request, 'accounts/reset.html', {'success': 'Password reset successful'})
        else:
            err = form.errors
            err = err['__all__']
            return render(request, 'accounts/reset.html', {'form': form, 'email': http.urlquote_plus(request.GET['id']), 'err': err})

def landing_view(request):
	username = request.session.get('username')
	if username == None:
		logged = 0
	else:
		logged = 1
	print(logged)
	if request.method == 'GET':
	    return render(request, 'landing.html', {'logged': logged})
