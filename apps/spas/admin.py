from django.contrib import admin
from .models import SpaOwner, Spa


@admin.register(SpaOwner)
class SpaOwnerAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'parent_owner', 'created_at']
    search_fields = ['fullname', 'parent_owner__fullname']
    raw_id_fields = ['parent_owner']
    ordering = ['fullname']


@admin.register(Spa)
class SpaAdmin(admin.ModelAdmin):
    list_display = ['spa_name', 'spa_code', 'owner', 'status', 'area', 'created_at']
    list_filter = ['status', 'area__city__state', 'area__city', 'area']
    search_fields = ['spa_name', 'spa_code', 'owner__fullname']
    raw_id_fields = ['owner', 'area', 'sub_owners', 'created_by']
    filter_horizontal = ['sub_owners']
    ordering = ['spa_name']
    fieldsets = (
        ('Basic', {'fields': ('spa_code', 'spa_name', 'status')}),
        ('Ownership', {'fields': ('owner', 'sub_owners')}),
        ('Location', {'fields': ('area', 'line_track', 'landmark', 'address')}),
        ('Contacts', {'fields': ('emails', 'phones')}),
        ('Dates', {'fields': ('opening_date', 'reopen_date')}),
        ('Agreement', {'fields': ('agreement_status', 'remark')}),
        ('Meta', {'fields': ('created_by', 'created_at')}),
    )
    readonly_fields = ['created_at']

# Register your models here.
