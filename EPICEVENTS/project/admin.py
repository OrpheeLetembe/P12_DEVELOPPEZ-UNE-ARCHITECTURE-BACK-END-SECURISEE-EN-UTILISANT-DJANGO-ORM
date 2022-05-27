from django.contrib import admin


from .models import Client, Contract, Event


class ClientAdmin(admin.ModelAdmin):

    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'sales_contact')
    list_filter = ('id', 'company_name', 'sales_contact')
    search_fields = ('company_name',)

    fieldsets = (
        (None, {'fields': ('company_name', 'phone')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile')}),
        ('Staff', {'fields': ('sales_contact',)})
    )


class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'status', 'amount', 'payment_due', 'sales_contact', 'date_created', 'date_updated')
    list_filter = ('status', 'client', 'sales_contact')
    search_fields = ('client', 'sales_contact')

    fieldsets = (
        (None, {'fields': ('client', 'sales_contact')}),
        ('Contract info', {'fields': ('amount', 'payment_due', 'status')}),
    )


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'contract', 'event_status', 'attendees', 'event_date', 'notes', 'support_contact',
                    'date_created', 'date_updated')
    list_filter = ('event_status', 'client', 'support_contact',)

    fieldsets = (
        (None, {'fields': ('client', 'contract')}),
        ('Event info', {'fields': ('event_date', 'attendees', 'notes', 'event_status')}),
        ('Staff', {'fields': ('support_contact',)})
    )


admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)

