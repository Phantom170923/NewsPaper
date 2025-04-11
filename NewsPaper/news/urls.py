from django.contrib import admin
from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
    path('news/create/', PostCreate.as_view(), {'post_type': 'news'}, name='create_news'),
    path('article/create/', PostCreate.as_view(), {'post_type': 'article'}, name='create_article'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='update_news'),
    path('article/<int:pk>/update/', PostUpdate.as_view(), name='update_article'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='delete_news'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='delete_article'),
]
