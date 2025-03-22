from email.mime import image
from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    ''' Encapsulate the data of a blog article by an author.'''

    # Define the data attributes of the Article object
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True) # url as a string
    image_file = models.ImageField(blank=True) # file upload
    
    def __str__(self):
        ''' Return a string representation of this model instance.'''
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        ''' Return a URL to display one instance of this object.'''
        return reverse('article', kwargs={'pk': self.pk})
    
    def get_all_comments(self):
        ''' Return all comments for this article.'''
        comments = Comment.objects.filter(article=self)
        return comments
    
class Comment(models.Model):
    ''' Encapsulate the data of a comment on a blog article.'''

    # data attributes of the Comment object
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        ''' Return a string representation of this Comment.'''
        return f'{self.text}'