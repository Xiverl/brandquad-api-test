from django.db import models


class NginxLog(models.Model):
    ip_address = models.GenericIPAddressField(
        verbose_name='ip-адрес'
    )
    date = models.DateTimeField(
        verbose_name='Дата'
    )
    http_method = models.CharField(
        verbose_name='Методы http',
        max_length=10
    )
    uri = models.TextField(
        verbose_name='URI'
    )
    status_code = models.IntegerField(
        verbose_name='Статус код'
    )
    response_size = models.IntegerField(
        verbose_name='Размер ответа'
    )

    def __str__(self):
        return f'{self.ip_address} - {self.date} - {self.uri}'
