from typing import Any, Optional
from django.core.management.base import BaseCommand

from graphbooks.models import Genre

class Command(BaseCommand):
    help = 'Fill genres'

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        genres = [
            ('Бизнес книги', 'FF8C00'),
            ('Классическая литература', 'FFE4B5'),
            ('Зарубежная литература', '4B0082'),
            ('Детские книги', '00FF00'),
            ('Детективы', '696969'),
            ('Фэнтези', '006400'),
            ('Фантастика', '20B2AA'),
            ('Юмористическая литература', 'FFD700'),
            ('Ужасы, мистика', 'FF0000'),
            ('Остросюжетная литература', 'C71585'),
        ]
        Genre.objects.bulk_create(
            Genre(name=name, color=color) for name, color in genres)