from celery import shared_task
import requests
import json
from datetime import datetime
from nginx_log.models import NginxLog
from django.db import transaction


@shared_task
def parse_and_save_log_file(file_url):
    """
    Асинхронный парсинг файла с конфигами
    и его сохранения в БД.
    """

    try:
        response = requests.get(file_url)
        response.raise_for_status()

        content = response.text.strip()

        if not content:
            return 'File is empty'

        processed_entries = 0
        with transaction.atomic():
            for line in content.split('\n'):
                if line.strip():
                    try:
                        log_data = json.loads(line)
                        NginxLog.objects.create(
                            ip_address=log_data['remote_ip'],
                            date=datetime.strptime(
                                log_data['time'],
                                '%d/%b/%Y:%H:%M:%S %z'
                            ),
                            http_method=log_data['request'].split()[0],
                            uri=log_data['request'].split()[1],
                            status_code=int(log_data['response']),
                            response_size=int(log_data['bytes'])
                        )
                        processed_entries += 1
                    except json.JSONDecodeError:
                        print(f'Не удалось разобрать JSON: {line}')
                    except KeyError as e:
                        print(f'Отсутствует ключ в JSON: {e}')
                        print(f'Проблемная запись: {line}')
                    except Exception as e:
                        print(f'Ошибка при обработке записи: {e}')
                        print(f'Проблемная запись: {line}')

        return f'Processed {processed_entries} log entries'

    except requests.RequestException as e:
        return f'Ошибка при получении файла: {str(e)}'
