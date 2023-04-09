from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .views import SignupForm


# Register your models here.
class MyUserModelAdmin(UserAdmin):
    add_form = SignupForm
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, MyUserModelAdmin)