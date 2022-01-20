from django import forms

class TokenForm(forms.Form):
    token=forms.CharField(label='Token',max_length=500)
