from django import forms
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
import re

class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm,self).__init__(*args, **kwargs)
        
        for field_name in ["username","password1","password2"]:
            self.fields[field_name].help_text = None
            
            
            
class CustomRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','confirm_password','email']
        
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        
        if len(password1) < 8:
            raise forms.ValidationError('Password must be atleast 8 characters long')
        
        
        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]', password1):
            raise forms.ValidationError('Password must be include Uppercase,Lowercase, number and special character')
        
        
    def clean(self):
        cleaned_data = super().clean()
        
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password1 != confirm_password:
            raise forms.ValidationError("Password do not matched")
        
        return cleaned_data
        