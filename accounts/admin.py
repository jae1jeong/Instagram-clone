from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile,FollowerRelation

class Followline(admin.StackedInline):
    model = FollowerRelation

class Profileline(admin.StackedInline):
    model = Profile
    con_delete = False # 프로필을 아예 없앨 수 있게 하는 속성

class CustomUserAdmin(UserAdmin):
    inlines = (Profileline,Followline)


admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)
