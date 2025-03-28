from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Author, Category, Post, PostCategory, Comment


# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'post'


