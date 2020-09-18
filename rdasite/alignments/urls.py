from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:review_supernote>_<str:rebuttal_supernote>/', views.detail, name='detail'),
]

