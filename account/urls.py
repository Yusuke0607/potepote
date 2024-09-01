from django.urls import path
from . import views
\
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('company_user_list/', views.company_user_list, name='company_user_list'),
    path('change_password/', views.change_password, name='change_password'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('notification/', views.notification_list, name='notification_list'),
    path('notification/<int:notification_id>/', views.notification_detail, name='notification_detail'),
]
