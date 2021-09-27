from django.shortcuts import render,redirect
from .models import Product, Order, Tag, Customer
from .forms import OrderForm

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


def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer': customer})
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'forms':form
    }

    return render(request, 'accounts/order_form.html', context)


def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'forms': form
    }

    return render(request, 'accounts/order_form.html', context)


def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {
        'item': order
    }
    return render(request, 'accounts/delete_form.html', context)
