from django.urls import path
from . import views
\
urlpatterns = [
    path('', views.inquiry, name='inquiry'),
    path('inquiry_complete/', views.inquiry_complete, name='inquiry_complete'),
]
