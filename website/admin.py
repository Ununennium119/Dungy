from django.contrib import admin
from website.models import *


class CostMemberInline(admin.StackedInline):
    model = CostMember


@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    inlines = [CostMemberInline]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(FriendRequest)
class FriendRequest(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
