from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from .models import CustomUser,Notification,UserNotification
from .forms import CustomUserCreationForm
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

""" Django 管理サイト名変更 """
admin.site.site_header = 'Me-Bias管理サイト'

""" サイト管理名変更 """
admin.site.index_title = 'データリスト'

class CustomUserResource(resources.ModelResource):
    メールアドレス = fields.Field(attribute='email', column_name='メールアドレス')
    アカウント名 = fields.Field(attribute='username', column_name='アカウント名')
    アクティブ = fields.Field(attribute='is_active', column_name='アクティブ')
    パスワード = fields.Field(attribute='password', column_name='パスワード')
    ユーザー種別 = fields.Field(attribute='user_type', column_name='ユーザー種別')

    class Meta:
        model = CustomUser
        fields = ('メールアドレス','アカウント名', 'アクティブ', 'パスワード','ユーザー種別')
        import_id_fields = ['メールアドレス']
        export_order = ('メールアドレス','アカウント名', 'アクティブ', 'パスワード','ユーザー種別')

    def before_save_instance(self, instance, using_transactions, dry_run):
        # パスワードが入力されている場合のみ暗号化
        if instance.password:
            instance.password = make_password(instance.password)

class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    add_form = CustomUserCreationForm
    resource_class = CustomUserResource
    list_display = ('email', 'user_type','username', 'is_active', 'is_superuser', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email','username', 'password')}),
        ('Permissions', {'fields': ( 'is_active', 'is_superuser', 'is_staff','user_type','groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username', 'password1', 'password2', 'is_staff', 'is_active', 'user_type','is_superuser', 'groups', 'user_permissions')}
        ),
    )
    readonly_fields = ("is_superuser",)
    search_fields = ('username', 'email',)
    ordering = ('username', 'email')

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_staff and not request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_staff and not request.user.is_superuser:
            return False
        return True

    def get_permissions(self, obj):
        return ", ".join([str(permission) for permission in obj.user_permissions.all()])

admin.site.register(CustomUser, CustomUserAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "content","created_at")
    search_fields = ("title", "content")
    readonly_fields = ("created_at",)

admin.site.register(Notification, NotificationAdmin)

class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "notification","is_read")
    search_fields = ("user", "notification","is_read")
    readonly_fields = ("user", "notification", "is_read",)

admin.site.register(UserNotification, UserNotificationAdmin)
