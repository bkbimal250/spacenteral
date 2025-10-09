from django.contrib import admin
from .models import Machine, AccountHolder


@admin.register(AccountHolder)
class AccountHolderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'designation', 'created_at']
    search_fields = ['full_name', 'designation']
    list_filter = ['designation', 'created_at']
    ordering = ['full_name']


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = [
        'serial_number', 'machine_code', 'machine_name', 'model_name',
        'spa_display', 'area_display', 'status', 'mid', 'tid',
        'created_at'
    ]
    list_filter = [
        'status', 'spa__area__city__state', 'spa__area__city', 'spa__area', 'model_name', 'bank_name',
        'created_at'
    ]
    search_fields = [
        'serial_number', 'machine_code', 'machine_name', 'model_name',
        'mid', 'tid', 'account_name', 'bank_name', 
        'acc_holder__full_name', 'acc_holder__designation',
        'spa__spa_name', 'spa__spa_code', 'remark'
    ]
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    autocomplete_fields = ['spa', 'acc_holder']
    
    fieldsets = (
        ('Machine Information', {
            'fields': (
                'serial_number', 'machine_code', 'machine_name',
                'model_name', 'firmware_version', 'status'
            )
        }),
        ('Spa & Location', {
            'fields': ('spa',),
            'description': 'Machine location (state, city, area) is inherited from the selected spa.'
        }),
        ('Banking & Account Information', {
            'fields': (
                'account_name', 'bank_name', 'account_number',
                'acc_holder', 'mid', 'tid'
            ),
            'classes': ('collapse',)
        }),
        ('Additional Info', {
            'fields': ('remark',),
            'classes': ('collapse',)
        }),
        ('Audit Information', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
    
    def spa_display(self, obj):
        return obj.spa.spa_name if obj.spa else '-'
    spa_display.short_description = 'Spa'
    spa_display.admin_order_field = 'spa__spa_name'
    
    def area_display(self, obj):
        """Display area inherited from spa"""
        if obj.spa and obj.spa.area:
            city_name = obj.spa.area.city.name if obj.spa.area.city else ''
            return f"{obj.spa.area.name} ({city_name})"
        return '-'
    area_display.short_description = 'Area (City)'
    area_display.admin_order_field = 'spa__area__name'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new machine
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['mark_in_use', 'mark_not_in_use', 'mark_broken']
    
    def mark_in_use(self, request, queryset):
        updated = queryset.update(status='in_use')
        self.message_user(request, f'{updated} machine(s) marked as In Use.')
    mark_in_use.short_description = 'Mark selected machines as In Use'
    
    def mark_not_in_use(self, request, queryset):
        updated = queryset.update(status='not_in_use')
        self.message_user(request, f'{updated} machine(s) marked as Not In Use.')
    mark_not_in_use.short_description = 'Mark selected machines as Not In Use'
    
    def mark_broken(self, request, queryset):
        updated = queryset.update(status='broken')
        self.message_user(request, f'{updated} machine(s) marked as Broken.')
    mark_broken.short_description = 'Mark selected machines as Broken'