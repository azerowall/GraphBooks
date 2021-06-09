from django.forms import ModelForm, Textarea

from .models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'rating', 'primary_genre', 'note', 'similar']
        widgets = {
            'note': Textarea(attrs={'rows': 4})
        }
