from django.db import models

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
