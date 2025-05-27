from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Extend the default User admin to include the Profile
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'profile__position')

# Unregister the default User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register Profile separately in case you want to manage it directly
admin.site.register(Profile)
