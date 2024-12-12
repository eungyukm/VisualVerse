from django.contrib import admin
from .models import Post, Image

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modify_dt')
    list_filter = ('modify_dt',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'image', 'created_at')