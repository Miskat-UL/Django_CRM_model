from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='product'),
    path('customers/<str:pk>', views.customers, name='customers'),
    path('create_order/<str:pk>', views.create_order, name='create_order'),
    path('update_order/<str:pk>', views.update_order, name='update'),
    path('delete_order/<str:pk>', views.delete_order, name='delete'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
