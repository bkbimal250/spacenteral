from django.contrib import admin
from .models import State, City, Area


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'created_at']
    list_filter = ['state']
    search_fields = ['name', 'state__name']
    raw_id_fields = ['state']
    ordering = ['state', 'name']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'created_at']
    list_filter = ['city__state', 'city']
    search_fields = ['name', 'city__name', 'city__state__name']
    raw_id_fields = ['city']
    ordering = ['city', 'name']

# Register your models here.
