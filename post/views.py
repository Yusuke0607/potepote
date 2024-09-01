from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import CustomUser
from .models import Post, PostRecipient
from django.http import JsonResponse
import random

@login_required
def my_posts(request):
    user_posts = Post.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'user_posts': user_posts,
    }
    return render(request, 'post/my_posts.html', context)
@login_required
def post_tweet(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content and len(content) <= 1000:
            post = Post.objects.create(user=request.user, content=content)

            # ランダムに他のユーザーに送信
            all_users = CustomUser.objects.exclude(id=request.user.id)  # カスタムユーザーモデルを使用
            recipients = random.sample(list(all_users), min(len(all_users), 5))  # 最大5人に送信

            for recipient in recipients:
                PostRecipient.objects.create(post=post, recipient=recipient)

            return redirect('my_posts')
    return render(request, 'post/post_tweet.html')

@login_required
def tweet_list(request):
    received_posts = PostRecipient.objects.filter(recipient=request.user,liked=False).select_related('post').order_by('-created_at')
    return render(request, 'post/tweet_list.html', {'received_posts': received_posts})

@login_required
def like_tweet(request, post_id):
    post_recipient = get_object_or_404(PostRecipient, post_id=post_id, recipient=request.user)
    post_recipient.liked = True
    post_recipient.save()
    return JsonResponse({'status': 'liked'})
