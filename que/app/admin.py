# yourappname/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Post,Friendship,ChatMessage
from django.utils.html import format_html
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    def get_friends_list(self, obj):
        friends_list = obj.friends.all()
        return format_html(', '.join([friend.username for friend in friends_list]))

    get_friends_list.short_description = 'Friends'

admin.site.register(CustomUser, CustomUserAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'content')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

admin.site.register(Post, PostAdmin)


class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'is_accepted', 'created_at')
    list_filter = ('created_at', 'is_accepted')
    search_fields = ('from_user__username', 'to_user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

admin.site.register(Friendship, FriendshipAdmin) 


admin.site.register(ChatMessage)