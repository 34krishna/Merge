from django.contrib import admin
from .models import*

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content','tag')
    list_filter = ('published_date', 'author')


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Tag)
