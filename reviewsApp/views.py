from django.shortcuts import render
from post.models import Post

def top(request):
    if request.user.is_authenticated:
        user = request.user
        user_posts = Post.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'reviewsApp/top.html', {'user_name': user,'user_posts': user_posts})
    else:
        return render(request, 'reviewsApp/top.html')

def terms_of_service(request):
    return render(request, 'reviewsApp/terms_of_service.html')

def privacy_policy(request):
    return render(request, 'reviewsApp/privacy_policy.html')

def operation_info(request):
    return render(request, 'reviewsApp/operation_info.html')

def error_404page(request, exception):
    return render(request, 'reviewsApp/404.html', status=404)

def error_500page(request):
    return render(request, 'reviewsApp/500.html', status=500)
