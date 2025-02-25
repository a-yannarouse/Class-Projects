# Description: define the forms that we use for create/update/delete operations.
from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    ''' Form to add a new article to the database.'''
    
    class Meta:
        ''' Define the model and fields of the form.'''
        model = Article
        fields = ['title', 'author', 'text', 'image_url']

class CreateCommentForm(forms.ModelForm):
    ''' Form to add a new comment to the database.'''
    
    class Meta:
        ''' Define the model and fields of the form.'''
        model = Comment
        fields = ['author', 'text',]