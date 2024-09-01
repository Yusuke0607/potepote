from django.urls import path
from . import views

urlpatterns = [
    path('post_tweet/', views.post_tweet, name='post_tweet'),
    path('tweet_list/', views.tweet_list, name='tweet_list'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('like/<int:post_id>/', views.like_tweet, name='like_tweet'),
]
