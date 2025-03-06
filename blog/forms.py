# Description: define the forms that we use for create/update/delete operations.
from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    ''' Form to add a new article to the database.'''
    
    class Meta:
        ''' Define the model and fields of the form.'''
        model = Article
        fields = ['title', 'author', 'text', 'image_file']

class UpdateArticleForm(forms.ModelForm):
    ''' A form to handle an update to an Article.'''
    
    class Meta:
        ''' Associate this form with a model in our database.'''
        model = Article
        fields = ['title', 'text',]

class CreateCommentForm(forms.ModelForm):
    ''' Form to add a new comment to the database.'''
    
    class Meta:
        ''' Define the model and fields of the form.'''
        model = Comment
        fields = ['author', 'text',]