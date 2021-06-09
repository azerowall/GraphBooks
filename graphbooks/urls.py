from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('interactive_map/', views.common_graph, name='common_graph'),
    path('graph/', views.graph, name='graph'),
    path('book/', views.book, name='book'),
    path('registration/', views.registration, name='registration')
]