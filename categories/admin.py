from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('category_id',)
    ordering= ('title',)
    # list_display = ('title')
    search_fields = ('title',)
    # prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category,CategoryAdmin)
