import random
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article

# Create your views here.
class ShowAllView(ListView):
    ''' Define a view class to show all blog articles. '''
    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):
    ''' Display a single article. '''
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" # note singular variable name

class RandomArticleView(DetailView):
    ''' Display a single article selected at random.'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" # note singular variable name

    def get_object(self):
        ''' Return one instance of the Article model selected at random.'''
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article