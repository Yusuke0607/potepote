from django.contrib import admin
from .models import Inquiry

class InquiryAdmin(admin.ModelAdmin):
    list_display = ("company_name", "first_name", "last_name", "email","content",'created_at')
    search_fields = ("company_name", "first_name", "last_name",  "email","content",'created_at')
    readonly_fields = ("company_name", "first_name", "last_name", "email","content",'created_at')

admin.site.register(Inquiry, InquiryAdmin)
