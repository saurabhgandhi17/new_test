from django.contrib import admin
from .models import GroupInfoModel, PrivateMessagesModel, GroupMessagesModel,PrivateGroupMessagesModel


@admin.register(GroupInfoModel)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_by']


@admin.register(GroupMessagesModel)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'sender', 'participants', 'group', 'created_at']


@admin.register(PrivateGroupMessagesModel)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'sender', 'receiver','created_at']


@admin.register(PrivateMessagesModel)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'sender', 'receiver', 'created_at']
