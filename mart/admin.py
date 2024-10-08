from django.contrib import admin
from mart.models import App, Author, AppRating, AppComment, UserProfile, DiscountUser, Discount


# Register your models here.


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'description', 'price', 'genre', 'created_at']
    list_filter = ['title', 'description', 'created_at', 'updated_at', 'price', 'genre']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AppRating)
class RatingAdmin(admin.ModelAdmin):
    list_filter = ['app', 'rating']

@admin.register(AppComment)
class AppCommentAdmin(admin.ModelAdmin):
    list_display = ['app','user','comment']
    list_filter = ['app','user','comment']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','name','surname','email']


@admin.register(DiscountUser)
class DiscountUserAdmin(admin.ModelAdmin):
    list_display = ['app','user','discount']

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name','percent']

