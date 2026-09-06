from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render,redirect
from django.db import models
from django.contrib.auth import authenticate, login
from .models import Product,Category, Supplier, Purchase, Sale

def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        sku = request.POST['sku']
        price = request.POST['price']
        stock_quantity = request.POST['stock_quantity']
        minimum_stock = request.POST['minimum_stock']
        category_id = request.POST['category']


        Product.objects.create(
    name=name,
    category_id=category_id,
    sku=sku,
    price=price,
    stock_quantity=stock_quantity,
    minimum_stock=minimum_stock
)



      
        return redirect('product_list')

    categories = Category.objects.all()
    return render(request, 'inventory/add_product.html', {'categories': categories})


def edit_product(request, id):
    product = Product.objects.get(id=id)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.name = request.POST['name']
        product.category_id = request.POST['category']
        product.sku = request.POST['sku']
        product.price = request.POST['price']
        product.stock_quantity = request.POST['stock_quantity']
        product.minimum_stock = request.POST['minimum_stock']

        product.save()

        return redirect('product_list')

    return render(
        request,
        'inventory/edit_product.html',
        {
            'product': product,
            'categories': categories
        }
    )




def delete_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'inventory/delete_product.html', {'product': product})


@login_required


def dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()

    low_stock_products = Product.objects.filter(
        stock_quantity__lte=models.F("minimum_stock")
    ).count()

    return render(request, 'inventory/dashboard.html', {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'low_stock_products': low_stock_products,
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'inventory/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')