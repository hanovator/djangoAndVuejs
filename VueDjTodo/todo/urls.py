
from django.urls import path

from . import views

app_name = 'todo'
urlpatterns = [
    path('vue_todo/', views.TodoTV.as_view(), name='vue_todo'),
]
