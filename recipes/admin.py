from django.contrib import admin
from .models import Recipe


class ListRecipes(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'published')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('category',)
    list_editable = ('published',)
    list_per_page = 5


admin.site.register(Recipe, ListRecipes)
