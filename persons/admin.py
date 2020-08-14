from django.contrib import admin
from .models import Person


class Persons(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 2


admin.site.register(Person, Persons)
