from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('adminReviewsApp/', admin.site.urls),
    path('account/', include('account.urls')),
    path('inquiry/', include('inquiry.urls')),
    path('', include('post.urls')),
    path('', views.top, name='top'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('operation_info/', views.operation_info, name='operation_info'),
]

handler404 = views.error_404page
handler500 = views.error_500page
