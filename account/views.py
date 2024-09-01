from django.contrib.auth import authenticate, login as user_login, logout as user_logout ,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm,CustomUser
from .models import Notification,UserNotification
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

def login(request):
    error_message = ''
    form = CustomAuthenticationForm()

    if request.user.is_authenticated:
        return redirect('top')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print(form)
            user = form.get_user()
            print(user)
            user_login(request, user)
            return redirect('top')
        else:
            # フォームのエラーメッセージを取得
            error_message = form.non_field_errors() or 'メールアドレスまたはパスワードが正しくありません。'

    return render(request, 'account/login.html', {'form': form, 'error_message': error_message})

@login_required
def logout(request):
    user_logout(request)
    return redirect('top')

@login_required
def edit_profile(request):
    error_message = ''
    username = request.user.username

    if request.method == 'POST':
        form = CustomUserChangeForm(data=request.POST, instance=request.user)
        new_email = request.POST.get('email')
        if new_email != request.user.email and CustomUser.objects.filter(email=new_email).exists():
            error_message = '入力されたメールアドレスはすでに使用されています。他のメールアドレスを使用してください。'
        else:
            if form.is_valid():
                form.save()
                return redirect('edit_profile')
            else:
                # フォームのエラーをコンソールに表示
                print(form.errors)
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'account/edit_profile.html', {'form': form,'username': username,'error_message': error_message})

@login_required
def change_password(request):
    error_message = ''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('edit_profile')
        else:
            old_password_errors = form.errors.get('old_password')
            password1_errors = form.errors.get('new_password1')
            password2_errors = form.errors.get('new_password2')

            if old_password_errors:
                error_message += f" 現在のパスワード: {', '.join(old_password_errors)}"
            if password1_errors:
                error_message += f" 新しいパスワード: {', '.join(password1_errors)}"
            if password2_errors:
                error_message += f" 新しいパスワード（確認）: {', '.join(password2_errors)}"

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {'form': form, 'error_message': error_message})


class PasswordReset(PasswordResetView):
    subject_template_name = 'account/mail_template/reset/subject.txt'
    email_template_name = 'account/mail_template/reset/message.txt'
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            error_message = '入力したメールアドレスは登録されていません。入力内容をご確認ください'
            return HttpResponseBadRequest(render(self.request, self.template_name, {'form': form, 'error_message': error_message}))
        else:
            return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseBadRequest(render(self.request, self.template_name, {'form': form, 'error_message': form.errors}))

class PasswordResetDone(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'account/password_reset_confirm.html'

    def form_invalid(self, form):
        return HttpResponseBadRequest(render(self.request, self.template_name, {'form': form, 'error_message': form.errors}))

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


@login_required
def company_user_list(request):
    users = CustomUser.objects.filter(company=request.user.company)
    return render(request, 'account/company_user_list.html', {'users': users})

@login_required
def create_company_user(request):
    if not request.user.is_company_admin:
        return redirect('company_user_list')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.company = request.user.company
            user.save()
            return redirect('company_user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'company_user_form.html', {'form': form})

@login_required
def edit_company_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id, company=request.user.company)

    if not request.user.is_company_admin:
        return redirect('company_user_list')

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('company_user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'company_user_form.html', {'form': form})

@login_required
def delete_company_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id, company=request.user.company)

    if not request.user.is_company_admin:
        return redirect('company_user_list')

    if request.method == 'POST':
        user.delete()
        return redirect('company_user_list')
    return render(request, 'confirm_delete.html', {'object': user})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification, UserNotification

@login_required
def notification_list(request):
    return render(request, 'account/notification_list.html')

@login_required
def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)

    # 通知を既読にする
    user_notification, created = UserNotification.objects.get_or_create(user=request.user, notification=notification)
    user_notification.is_read = True
    user_notification.save()

    return render(request, 'account/notification_detail.html', {'notification': notification})
