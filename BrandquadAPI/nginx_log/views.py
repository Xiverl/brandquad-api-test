from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from nginx_log.models import NginxLog
from nginx_log.serializers import NginxLogSerializer, LogFileSerializer
from nginx_log.tasks import parse_and_save_log_file
from nginx_log.filters import NginxLogFilter
from nginx_log.pagination import CustomPagination
from nginx_log.utils import download_file


class NginxLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для обработки файла с конфигами
    nginx, а также для его отображения.
    """

    queryset = NginxLog.objects.all()
    serializer_class = NginxLogSerializer
    http_method_names = ['get', 'post']
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NginxLogFilter

    @action(detail=False, methods=['post'])
    def upload_log(self, request):
        serializer = LogFileSerializer(data=request.data)
        if serializer.is_valid():
            file_url = download_file(serializer.validated_data['file_url'])
            parse_and_save_log_file.delay(file_url)
            return Response(
                {'status': 'Log parsing started'},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        log_entry = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(log_entry)
        return Response(serializer.data)
