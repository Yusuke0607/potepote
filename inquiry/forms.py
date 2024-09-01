from django import forms
from .models import Inquiry

class InquiryForm(forms.Form):
    company_name = forms.CharField(label='会社名', max_length=30)
    first_name = forms.CharField(label='名', max_length=30)
    last_name = forms.CharField(label='名', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    phone_number = forms.CharField(label='名', max_length=20)
    content = forms.CharField(label='問い合わせ内容',widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
