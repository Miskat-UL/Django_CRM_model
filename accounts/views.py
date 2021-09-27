from django.shortcuts import render
from .models import Product, Order, Tag, Customer

def home(request):
    customer = Customer.objects.all()
    order = Order.objects.all()
    total_customers = customer.count()
    total_order = order.count()
    delivered = order.filter(status="Delivered").count()
    pending = order.filter(status="pending").count()
    context = {
        'customers': customer,
        'orders': order,
        'total_order': total_order,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)


def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    context = {
        'customers': customer,
        'orders': orders
    }
    return render(request, 'accounts/customer.html', context)

