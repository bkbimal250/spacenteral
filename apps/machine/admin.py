from django.contrib import admin
from .models import Machine, MachineAssignment


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'model_name', 'spa', 'installed_area', 'status', 'created_at']
    list_filter = ['status', 'installed_area__city__state', 'installed_area__city', 'installed_area', 'spa']
    search_fields = ['serial_number', 'model_name', 'spa__spa_name']
    raw_id_fields = ['spa', 'installed_area', 'created_by']
    ordering = ['serial_number']


@admin.register(MachineAssignment)
class MachineAssignmentAdmin(admin.ModelAdmin):
    list_display = ['machine', 'from_spa', 'to_spa', 'from_area', 'to_area', 'moved_at']
    list_filter = ['to_spa', 'to_area']
    search_fields = ['machine__serial_number', 'from_spa__spa_name', 'to_spa__spa_name']
    raw_id_fields = ['machine', 'from_spa', 'to_spa', 'from_area', 'to_area']
    ordering = ['-moved_at']

# Register your models here.
