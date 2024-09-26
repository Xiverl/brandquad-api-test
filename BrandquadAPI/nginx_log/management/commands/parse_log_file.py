from django.core.management.base import BaseCommand
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from nginx_log.utils import download_file
from nginx_log.tasks import parse_and_save_log_file


class Command(BaseCommand):
    help = 'Process a given URL'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL to process')

    def handle(self, *args, **options):
        url = options['url']

        # Валидация URL
        validate = URLValidator()
        try:
            validate(url)
        except ValidationError:
            self.stderr.write(self.style.ERROR(f'Invalid URL: {url}'))
            return

        try:
            # Обработка URL
            file_url = download_file(url)
            self.stdout.write(self.style.SUCCESS(
                    f'Обработка url прошла успешно!: {url}'
                )
            )
            parse_and_save_log_file.delay(file_url)
            self.stdout.write(
                'Данные из лог файла парсятся и добавляются в БД...'
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(
                    f'Error processing URL {url}: {str(e)}'
                )
            )
