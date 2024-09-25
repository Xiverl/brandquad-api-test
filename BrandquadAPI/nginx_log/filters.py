from django_filters import rest_framework as filters

from nginx_log.models import NginxLog


class NginxLogFilter(filters.FilterSet):
    min_date = filters.DateFilter(field_name="timestamp", lookup_expr='gte')
    max_date = filters.DateFilter(field_name="timestamp", lookup_expr='lte')
    ip_address = filters.CharFilter(
        field_name="ip_address", lookup_expr='icontains'
    )

    class Meta:
        model = NginxLog
        fields = ['min_date', 'max_date', 'ip_address', 'status_code']
