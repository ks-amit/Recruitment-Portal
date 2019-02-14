from . import models
from django import forms
from django.core import validators
from accounts import models as account_models
from django.utils import timezone

class SetterRequest(forms.ModelForm):
    description = forms.CharField(required=True, max_length=1000, widget=forms.Textarea(attrs={'placeholder': 'Your Description Here'}))

    class Meta:
        model = models.setter_request
        fields = ['description']


class CreateChallenge(forms.ModelForm):
    name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Contest Name'}))
    slug = forms.SlugField(required=True, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'URL'}))

    class Meta:
        model = models.challenge
        fields = ['name', 'slug']

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        try:
            dv = validators.validate_slug(slug)
        except:
            raise forms.ValidationError("Please enter a valid URL")
        match = models.challenge.objects.filter(slug=slug)
        if(len(match) != 0):
            raise forms.ValidationError("URL already exists. Please enter a different URL.")
        else:
            return slug

class challengeDetails(forms.ModelForm):
    name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'readonly': 'true', 'placeholder': 'Contest Name'}))
    slug = forms.SlugField(required=True, max_length=50, widget=forms.TextInput(attrs={'readonly': 'true'}))
    type = forms.ChoiceField(choices=(('O', 'Open'), ('P', 'Private'),))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    instructions = forms.CharField(max_length=2000, required=False, widget=forms.Textarea(attrs={'placeholder': 'Challenge Instructions'}))

    class Meta:
        model = models.challenge
        fields = ['name', 'slug', 'type', 'start_time', 'end_time', 'start_date', 'end_date', 'instructions']

class extendChallenge(forms.ModelForm):
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = models.challenge
        fields = ['end_date', 'end_time']

    def clean(self):
        try:
            curr_date = timezone.now().date()
            curr_time = timezone.now().time()
            end_date = self.cleaned_data['end_date']
            end_time = self.cleaned_data['end_time']
            if end_date > curr_date:
                return self.cleaned_data
            elif end_date == curr_date and end_time > curr_time:
                return self.cleaned_data
            else:
                raise forms.ValidationError("Invalid Time Input")
        except:
            raise forms.ValidationError("Invalid Time Input")

class newQuestion(forms.ModelForm):
    name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Question Name'}))
    slug = forms.SlugField(required=True, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'CODE'}))
    points = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Points'}))
    difficulty = forms.ChoiceField(choices=(('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard'),))
    statement = forms.CharField(max_length=2000, required=True, widget=forms.Textarea(attrs={'placeholder': 'Question Statement'}))
    option1 = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Option A'}))
    option2 = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Option B'}))
    option3 = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Option C'}))
    option4 = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Option D'}))
    tags = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'Tags'}))
    answer = forms.MultipleChoiceField(choices=(('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),), widget=forms.CheckboxSelectMultiple())
    editorial = forms.CharField(max_length=2000, required=False, widget=forms.Textarea(attrs={'placeholder': 'Question Editorial'}))

    class Meta:
        model = models.question
        fields = ['name', 'slug', 'points', 'difficulty', 'statement', 'option1', 'option2', 'option3', 'option4', 'tags', 'answer', 'editorial']

    def clean(self):
        slug = self.cleaned_data['slug']
        try:
            dv = validators.validate_slug(slug)
        except:
            raise forms.ValidationError("Please enter a valid URL")
        match = models.question.objects.filter(slug=slug)
        if(len(match) != 0):
            raise forms.ValidationError("URL already exists. Please enter a different URL.")
        else:
            answer = self.cleaned_data.get('answer')
            if answer == None:
                raise forms.ValidationError("Check the correct answers for the question.")
            else:
                return self.cleaned_data

class manageQuestion(newQuestion):
    slug = forms.SlugField(required=True, max_length=50, widget=forms.TextInput(attrs={'readonly': 'true'}))

    def clean(self):
        slug = self.cleaned_data['slug']
        try:
            dv = validators.validate_slug(slug)
        except:
            raise forms.ValidationError("Please enter a valid URL")

        answer = self.cleaned_data.get('answer')
        if answer == None:
            raise forms.ValidationError("Check the correct answers for the question.")
        else:
            return self.cleaned_data

class manageQuestionAdmin(newQuestion):
    name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Question Name', 'readonly': 'true'}))
    slug = forms.SlugField(required=True, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'CODE', 'readonly': 'true'}))
    points = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Points', 'readonly': 'true'}))
    difficulty = forms.ChoiceField(choices=(('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard'),))
    statement = forms.CharField(max_length=2000, required=True, widget=forms.Textarea(attrs={'placeholder': 'Question Statement', 'readonly': 'true'}))
    option1 = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Option A', 'readonly': 'true'}))
    option2 = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Option B', 'readonly': 'true'}))
    option3 = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Option C', 'readonly': 'true'}))
    option4 = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Option D', 'readonly': 'true'}))
    tags = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'Tags', 'readonly': 'true'}))
    answer = forms.MultipleChoiceField(choices=(('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),), widget=forms.CheckboxSelectMultiple(attrs={'readonly': 'true'}))
    editorial = forms.CharField(max_length=2000, required=False, widget=forms.Textarea(attrs={'placeholder': 'Question Editorial', 'readonly': 'true'}))

class newCollaborator(forms.ModelForm):
    setter = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))

    def clean(self):
        setter = self.cleaned_data['setter']
        print(setter)
        match = account_models.user.objects.filter(username=setter)
        if len(match) == 0:
            raise forms.ValidationError("The provided user cannot be added as a collaborator.")
        else:
            return self.cleaned_data

    class Meta:
        model = models.challenge_setter
        fields = ['setter']

class newSubmission(forms.ModelForm):
    answer = forms.MultipleChoiceField(required=False, choices=(('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = models.submission
        fields = ['answer']

class removeChallenge(forms.ModelForm):
    oldpassword = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'}))

    class Meta:
        model = account_models.user
        fields = ['oldpassword']

#Parag
class AccountForm(forms.ModelForm):

    username = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'UserName'}))
    firstname = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    lastname = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    bio = forms.CharField(required=False,widget=forms.Textarea(attrs={'placeholder': 'Please enter the  description about yourself!'}))
    #address = forms.CharField(required=True, max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    contactno = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Contact No.'}))
    image = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'profile_pic','id':'pro_pic'}))

    class Meta:
        model = account_models.user
        fields = ['username', 'email', 'firstname', 'lastname', 'bio', 'contactno','image']

    def clean_contactno(self):
        contactno = self.cleaned_data['contactno']
        contactno = str(contactno)
        if len(contactno) != 10:
            raise forms.ValidationError("Contact number invalid")
        else:
            return self.cleaned_data['contactno']   

class ChangePassword(forms.ModelForm):

    # username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'})) 
    oldpassword = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Old Password'}))
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'New Password'}))
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = account_models.user
        fields = ['oldpassword', 'password1', 'password2']
      
        
    def clean_password2(self):
        pas1 = self.cleaned_data['password1']
        pas2 = self.cleaned_data['password2']
        if len(pas1) == 0 or len(pas2) == 0:
            raise forms.ValidationError("Fields cannot be empty")
        elif pas1 != pas2:
            raise forms.ValidationError("Passwords Do Not Match")
        return pas1    