from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.home),
    path('products/', views.products),
    path('customers/', views.customers),
]
