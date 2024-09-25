from rest_framework import serializers
from nginx_log.models import NginxLog


class NginxLogSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображени информации
    по конфигам nginx.
    """

    class Meta:
        model = NginxLog
        fields = '__all__'


class LogFileSerializer(serializers.Serializer):
    """
    Сериализатор для обработки ссылки на файл
    с конфигами nginx.
    """

    file_url = serializers.URLField()
