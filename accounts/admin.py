from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import site

from accounts.forms import AccountCreationForm, AccountChangeForm

User = get_user_model()


class AccountAdmin(UserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm
    model = User
    list_display = ['username', 'name', 'is_staff', 'role']
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("name", 'role')}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("name", 'role')}),)


site.register(User, AccountAdmin)
