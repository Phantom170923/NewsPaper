from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = sum(post.rating for post in self.post_set.all()) * 3

        comment_rating = sum(comment.rating for comment in self.user.comment_set.all())

        post_comment_rating = sum(
            comment.rating
            for post in self.post_set.all()
            for comment in post.comment_set.all()
        )
        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name_category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name_category


class Post(models.Model):
    news_or_article = [('news', 'новость'), ('article', 'статья')]

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    choice = models.CharField(max_length=7, choices=news_or_article)
    time_in = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) < 124:
            return self.text
        else:
            return self.text[:124] + '...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

