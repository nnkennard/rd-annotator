from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:parent_supernote>_<str:comment_supernote>/', views.detail, name='detail'),
]

