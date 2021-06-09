from typing import Any, Optional
from django.core.management.base import BaseCommand

from graphbooks.models import Genre, Book, get_user_for_common_graph

import openpyxl

class Command(BaseCommand):
    help = 'Import books and genres from xslx'

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        user = get_user_for_common_graph()

        workbook = openpyxl.load_workbook('Graphbooks.xlsx', data_only=True)
        sheet = workbook['Sheet1']

        genres = dict()
        books = dict()
        similar = dict()

        i = 10
        for row in sheet.iter_rows(min_row=2, min_col=1, max_col=6, values_only=True):
            name, _, genre_name, rating, similar_names, note = row

            rating = int(rating) if rating != None else 0

            if similar_names is not None:
                similar_names = [n.strip() for n in similar_names.split(';')]
            else:
                similar_names = []
            
            if note is None:
                note = ''

            print('Add book', name)
            #genres.setdefault(genre_name, Genre(name=genre_name))
            genre = genres.get(genre_name, None)
            if genre is None:
                print('Add genre', genre_name)
                genre = Genre(name=genre_name)
                genre.save()
                genres[genre_name] = genre

            book = Book(user=user, name=name, primary_genre=genre, rating=rating, note=note)
            book.save()
            books[name] = book

            similar[name] = similar_names

        print('update m2m')
        for book_name, similar_names in similar.items():
            book = books[book_name]
            for sim_name in similar_names:
                sim_book = books.get(sim_name, None)
                if sim_book is None:
                    print(f"Similar book '{sim_name}' for '{book_name}' not found in imported books")
                else:
                    book.similar.add(books[sim_name])
            book.save()
        
        
        '''
        Genre.objects.bulk_create(genres.values())

        # обновление id жанров
        genres_list = Genre.objects.all()
        genres.clear()
        for genre in genres_list:
            genres[genre.name] = genre
        
        # обновление id жанров книг
        for book in books.values():
            book.primary_genre.pk = genres[book.primary_genre.name].pk

        Book.objects.bulk_create(book.values())

        # обновление id книг
        books_list = 
        '''

