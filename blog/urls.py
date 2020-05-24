from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name='blogindex'),
    path("blogpost/<int:id>", views.blogpost, name='blogpost'),
    ]