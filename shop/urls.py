from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name='Shopindex'),
    path("about/", views.about, name='AboutUs'),
    path("contact/", views.Contact, name='ContactUs'),
    path("tracker/", views.tracker, name='TrackingStatus'),
    path("search/", views.search, name='Search'),
    path("products/<int:myid>", views.productview, name='ProductView'),
    path("checkout/", views.checkout, name='Checkout')
    
    ]