from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User

#logo = 'static/Logo.png'

admin.site.site_header = 'Epic Events'
admin.site.site_title = 'Epic Evens - Management Interface'
admin.site.index_tilte = 'CRM - Management Interface',


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'mobile', 'team', 'groups')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'mobile', 'team')


class AdminUser(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'username', 'first_name', 'last_name', 'mobile', 'email', 'team')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile')}),
        ('Permissions', {'fields': ('team', 'groups')})
    )
    search_fields = ('username', 'team')


admin.site.register(User, AdminUser)

