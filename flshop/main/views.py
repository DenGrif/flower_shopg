from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, AddToCartForm, OrderForm
from .models import Flower, Order
from .utils import send_order_notification_to_telegram
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    flowers = Flower.objects.all()
    context = {
        'flowers': flowers
    }
    return render(request, 'home.html', context)

@login_required
def add_to_cart(request, pk):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            flower = Flower.objects.get(pk=pk)
            order, created = Order.objects.get_or_create(user=request.user, flower=flower, defaults={'quantity': quantity})
            if not created:
                order.quantity += quantity
                order.save()
            return redirect('view_cart')
    else:
        form = AddToCartForm()
    return render(request, 'add_to_cart.html', {'form': form, 'flower': Flower.objects.get(pk=pk)})

@login_required
def view_cart(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, 'view_cart.html', context)

@login_required
def remove_from_cart(request, pk):
    order = Order.objects.get(pk=pk)
    order.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            delivery_date_time = form.cleaned_data['delivery_date_time']
            address = form.cleaned_data['address']
            comment = form.cleaned_data['comment']
            orders = Order.objects.filter(user=request.user)
            for order in orders:
                order.delivery_date_time = delivery_date_time
                order.address = address
                order.comment = comment
                order.save()
            # Здесь будем вызывать функцию отправки уведомления в Telegram
            send_order_notification_to_telegram(orders)
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'checkout.html', {'form': form})

def order_success(request):
    return render(request, 'order_success.html')