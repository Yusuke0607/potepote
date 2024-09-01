from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm,UserChangeForm,PasswordChangeForm,UserCreationForm
from django.contrib.auth import authenticate

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        password = self.data.get('password')

        if email and password:
            user = authenticate(self.request, username=email, password=password)
            if user is None:
                raise ValidationError('メールアドレスまたはパスワードが正しくありません。')

        return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email","username","password1", "password2")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = ''

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username","email")

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
