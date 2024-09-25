from django.contrib import admin
from .models import NginxLog


@admin.register(NginxLog)
class NginxLogAdmin(admin.ModelAdmin):
    list_display = (
        'ip_address', 'date', 'http_method',
        'uri', 'status_code', 'response_size'
    )
    list_filter = ('http_method', 'status_code')
    search_fields = ('ip_address', 'uri')
