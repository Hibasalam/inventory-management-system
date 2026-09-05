from django.shortcuts import render,redirect
from .models import Product

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

        Product.objects.create(
            name=name,
            sku=sku,
            price=price,
            stock_quantity=stock_quantity,
            minimum_stock=minimum_stock
        )

        return redirect('product_list')

    return render(request, 'inventory/add_product.html')

def edit_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.sku = request.POST['sku']
        product.price = request.POST['price']
        product.stock_quantity = request.POST['stock_quantity']
        product.minimum_stock = request.POST['minimum_stock']

        product.save()

        return redirect('product_list')

    return render(request, 'inventory/edit_product.html', {'product': product})



def delete_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'inventory/delete_product.html', {'product': product})