from django.contrib import admin
from website.models import *


# Register your models here.

@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    pass