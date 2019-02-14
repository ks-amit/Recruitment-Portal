from . import models
from django import forms
from django.core import validators
from django.contrib.auth.hashers import check_password

class UserCreate(forms.ModelForm):

    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(max_length=100, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = models.user
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        match = models.user.objects.filter(username=username)
        if len(match) != 0:
            raise forms.ValidationError("Username already exists")
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            dv = validators.validate_email(email)
        except:
            raise forms.ValidationError("Please enter a valid email")
        match = models.user.objects.filter(email=email)
        if(len(match) != 0):
            raise forms.ValidationError("Email already registered")
        else:
            return email

    def clean_password2(self):
        pas1 = self.cleaned_data['password1']
        pas2 = self.cleaned_data['password2']
        if len(pas1) == 0 or len(pas2) == 0:
            raise forms.ValidationError("Fields cannot be empty")
        elif pas1 != pas2:
            raise forms.ValidationError("Passwords do not match")
        return pas1

class UserLogin(forms.ModelForm):

    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = models.user
        fields = ['username', 'password']

    def clean(self):

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if username == '':
            raise forms.ValidationError("Username field cannot be empty.")
        else:
            match = models.user.objects.filter(username=username, activated=True)
            if len(match) == 0:
                raise forms.ValidationError("Username is not registered. Please register and activate before logging in.")
            else:
                if password == '':
                    raise forms.ValidationError("Password field cannot be empty.")
                else:
                    curr_user = match[0]
                    if check_password(password, curr_user.password) == True:
                        return self.cleaned_data
                    else:
                        raise forms.ValidationError("Incorrect Password. Make sure to check your Caps Lock.")

class UserForgot(forms.ModelForm):

    email = forms.EmailField(max_length = 100, required = True, widget = forms.EmailInput(attrs = {'placeholder': 'Registered Email'}))

    class Meta:
        model = models.user
        fields = ['email',]

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            dv = validators.validate_email(email)
        except:
            raise forms.ValidationError("Please enter a valid email")
        match = models.user.objects.filter(email=email)
        if(len(match) == 0):
            raise forms.ValidationError("Email is not registered. Please register to login.")
        else:
            return email

class UserReset(forms.ModelForm):

    password1 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    password2 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}))

    class Meta:
        model = models.user
        fields = ['password1', 'password2']

    def clean(self):

        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 == '' or password2 == '':
            raise forms.ValidationError("Any field cannot be empty")
        else:
            if password1 == password2:
                return self.cleaned_data
            else:
                raise forms.ValidationError("Passwords do not match")
