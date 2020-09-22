from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submitted/', views.submitted, name='submitted'),
    path('<str:review_supernote>_<str:rebuttal_supernote>/', views.detail, name='detail'),
    #path('<str:review_supernote>_<str:rebuttal_supernote>/submitted/', views.submitted, name='submitted'),
]

