from django import forms
from django.forms import fields
from django.forms.fields import EmailField

from blog.models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = EmailField()
    to = EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body') 