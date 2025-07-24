from django.contrib import admin
from .models import SerialRecord

@admin.register(SerialRecord)
class SerialRecordAdmin(admin.ModelAdmin):
    # Columns to show in the changelist
    list_display    = ('serial_number', 'worker_name', 'uploader', 'processed_at')
    # Enable search by SN or worker name
    search_fields   = ('serial_number', 'worker_name')
    # Add filters on uploader and by date
    list_filter     = ('uploader',)
    # Adds a date-based drill-down navigation by processed_at
    date_hierarchy  = 'processed_at'
    # Order most recent first
    ordering        = ('-processed_at',)
