from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, tweets
#Unregister the Group
admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):
    model = Profile

#Extend User Model
class UserAdmin(admin.ModelAdmin):
    model= User
    fields = ["username"]
    inlines = [ProfileInline]

#By default User unregister korchi
admin.site.unregister(User)

#Admin pannel e User, User admin show korar jonno register korchi
admin.site.register(User, UserAdmin)

admin.site.register(tweets)





