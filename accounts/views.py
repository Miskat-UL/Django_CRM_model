from django.shortcuts import render, redirect
from .models import Product, Order, Tag, Customer
from django.contrib.auth.forms import UserCreationForm
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.models import Group


@unauthenticated_user
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, "username or password in incorrect")

        context = {}
        return render(request, 'accounts/login.html', context)


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'User create successfull ' + username)
            return redirect('/login')
    context = {'forms': form}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()
    total_order = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="pending").count()
    print(orders)
    context = {'orders': orders, 'total_order': total_order,
               'delivered': delivered,
               'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'accounts/account_setting.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
# @allowed_user(allowed_roles=['Admin'])
@admin_only
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


@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    my_filters = OrderFilter(request.GET, queryset=orders)
    orders = my_filters.qs
    context = {
        'customers': customer,
        'orders': orders,
        'filter': my_filters
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer': customer})
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'forms': form
    }

    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {
        'item': order
    }
    return render(request, 'accounts/delete_form.html', context)
