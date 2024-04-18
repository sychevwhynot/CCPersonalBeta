from django.contrib import admin
from .models import Feedlist, Category

class FeedlistAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'time_create', 'time_update', 'is_published', 'user')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'content')
    readonly_fields = ('time_create', 'time_update', 'user')
    
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Feedlist, FeedlistAdmin)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
