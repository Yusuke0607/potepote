from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('superuser', 'スーパーユーザー'),
        ('admin', '管理者ユーザー'),
        ('user', '一般ユーザー'),
    ]

    email = models.EmailField(unique=True, verbose_name='メールアドレス')
    is_active = models.BooleanField(default=True, verbose_name='アカウント有効')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='user', verbose_name='ユーザー種別')

    # メールアドレスを一意キーにする。
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Inquiry(models.Model):
    company_name = models.CharField(max_length=100, verbose_name='お名前')
    first_name = models.CharField(max_length=100, verbose_name='名')
    last_name = models.CharField(max_length=100, verbose_name='姓')
    email = models.EmailField(verbose_name='連絡先メールアドレス')
    phone_number = models.CharField(max_length=20, verbose_name='電話番号')
    content = models.TextField(verbose_name='問い合わせ内容')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='問い合わせ日時')

    class Meta:
        verbose_name = 'お問い合わせ'
        verbose_name_plural = 'お問い合わせ一覧'

    def __str__(self):
        return f"Inquiry from {self.company_name} {self.first_name} {self.last_name} ({self.email})"

class Notification(models.Model):
    CATEGORY_CHOICES = [
        ('personal', 'あなたへのお知らせ'),
        ('product', 'プロダクト情報'),
        ('mebias', 'Me-Biasからのご案内'),
    ]
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='カテゴリ')

    class Meta:
        verbose_name = 'お知らせ'
        verbose_name_plural = 'お知らせ一覧'

    def __str__(self):
        return self.title

class UserNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'お知らせ既読'
        verbose_name_plural = 'お知らせ既読一覧'

    def __str__(self):
        return f'{self.user.username} - {self.notification.title}'
