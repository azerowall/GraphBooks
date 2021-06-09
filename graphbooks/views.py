from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Genre, Book, User, get_user_for_common_graph
from .forms import BookForm


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', dict(form=form))

def index(request):
    return render(request, 'graphbooks/index.html')

def about(request):
    return render(request, 'graphbooks/about.html')

def common_graph(request):
    return render(request, 'graphbooks/graph.html',
        dict(title='Интерактивная карта', editable=False, graph_ep='/graph/?common=1'))

@login_required
def profile(request):
    return render(request, 'graphbooks/graph.html',
        dict(title='Личный кабинет', editable=True, graph_ep='/graph/'))


def get_book_graph(user):
    '''
        Формирование графа для visjs
    '''
    books = user.books.all()
    nodes = []
    edges = set()

    for book in books:
        nodes.append({
            'id': book.id,
            'label': book.name,
            'value': book.rating,
            'group': str(book.primary_genre.id) if book.primary_genre else '',
        })

    # TODO: неэффектино
    for book in books:
        sim = book.similar.all()
        for sim_book in sim:
            if book.id == sim_book.id:
                continue
            id1, id2 = book.id, sim_book.id
            # сортировка для устранения двойных дуг (a, b) и (b, a)
            id1, id2 = min(id1, id2), max(id1, id2)
            edges.add((id1, id2))
    
    return {
        'nodes': nodes,
        'edges': [{'from': f, 'to': t} for f, t in edges]
    }


def graph(request):
    if 'common' in request.GET:
        user = get_user_for_common_graph()
    else:
        if request.user.is_authenticated:
            user = request.user
        else:
            return JsonResponse({'error': 'Login required'})

    graph = get_book_graph(user)
    
    return JsonResponse({'result': graph})


def book(request):
    if 'id' in request.GET:
        book_id = int(request.GET['id'])
        book = Book.objects.get(pk=book_id)

        allow = book.user == get_user_for_common_graph() or \
            (request.user.is_authenticated and request.user == book.user)
        if not allow:
            return JsonResponse({'error': 'Wrong book id'})
    else:
        book = Book(user=request.user)

    if request.method in ['POST', 'DELETE']:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Login required'})

    if 'form' in request.GET:
        if request.method == 'POST':
            form = BookForm(request.POST, instance=book)
            form.fields['similar'].queryset = book.user.books
            if form.is_valid():
                form.save()
                return JsonResponse({'result': True})
        else:
            form = BookForm(instance=book)
            form.fields['similar'].queryset = book.user.books
        return render(request, 'graphbooks/book_form.html', dict(form=form))
    elif 'info' in request.GET:
        return render(request, 'graphbooks/book_info.html', dict(book=book))
    else:
        if request.method == 'DELETE':
            book.delete()
        return JsonResponse({'result': True})
