from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User

admin.site.site_header = 'Epic Events'
admin.site.site_title = 'Epic Evens - Management Interface'
admin.site.index_tilte = 'CRM - Management Interface'


class AdminUser(UserAdmin):

    list_display = ('id', 'username', 'first_name', 'last_name', 'mobile', 'email', 'team')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile', 'team')}),
        ('Permissions', {'fields': ('is_staff', 'groups', 'is_active')})
    )
    search_fields = ('username', 'team')


admin.site.register(User, AdminUser)

