import os.path
from csv import DictReader

from django.conf import settings as st
from django.core.management import BaseCommand

from wireguard.models import AllowedIp, Dns


class Command(BaseCommand):
    help = "Команда для загрузки тестовых данных в БД из csv файлов"

    # Список переменных для импорта данных в модели
    models = (
        (
            (AllowedIp, 'allowed_ips'),
            (Dns, 'dns'),
        ),
    )

    def import_data(self):
        """ Импорт базовых данных в БД при развёртывании проекта. """

        for data in self.models:
            for model, file in data:
                file_path = os.path.join(st.BASE_DIR,
                                         f'static/data/{file}.csv')
                with open(file_path, encoding='utf-8') as f:
                    print(f'Начался импорт данных - {file}')
                    for row in DictReader(f):
                        model.objects.get_or_create(**row)
                print(f'Импорт данных - {file} завершен.')

    def handle(self, *args, **options):
        """ Агрегирующий метод, который вызывается с помощью команды import
        и добавляет тестовые данные в БД. """

        self.import_data()
