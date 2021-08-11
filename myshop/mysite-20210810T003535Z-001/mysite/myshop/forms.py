from django import forms
from .models import Memo

class SearchForm(forms.Form):
    itemName = forms.CharField(label='商品名', max_length=200, required=True)
    
class AddForm(forms.ModelForm):  
    class Meta:
        model = Memo
        fields ="__all__"
        labels={
            'name':'商品名',
            'dsc':'説明',
            'date':'日付',
            'pic':'IMG'
        }
        widgets = {
            'date': forms.SelectDateWidget
        }
        
class SearchAForm(forms.Form):
    name = forms.CharField(label='商品名', max_length=200)
    
class SearchBForm(forms.Form):    
    date = forms.DateField(label='日付')
    

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
