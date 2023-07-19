import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import SignupForm, NewProductForm, EditProductForm
import datetime
# Create your views here.
def signup(request):
    if request.method == 'POST':
        print("post method")
        print(request.body)
        form = SignupForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()

            return redirect('../login/')
    else:
        form = SignupForm()
    context ={ 'form':form }
    return render(request, 'store/signup.html', context)

@login_required
def dashboard(request):
    products = Product.objects.filter(vendor=request.user)

    return render(request, 'store/dashboard.html', {'products':products})

@login_required
def delete_product(request,pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    product.delete()
    return redirect('../../dashboard')

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    if request.method == "POST":
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('detail', pk=product.id)

    else:
        form = EditProductForm(instance=product)
        return render(request, 'store/form.html', {'form':form, 'title':'Edit Item'})

@login_required
def new_product(request):
    if request.method == "POST":
        form = NewProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()

            return redirect('detail', pk=product.id)
    else:
        form = NewProductForm()
        return render(request, 'store/form.html', {'form':form, 'title':'New Item'})

def store(request):
    if request.user.is_authenticated:
        if not hasattr(request.user, 'customer'):
            customer = Customer.objects.create(
                user = request.user,
                name = request.user.username,
                email = request.user.email
            )
        else:
            customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total': 0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products':products, 'cartItems':cartItems, 'categories':categories}
    return render(request, 'store/store.html', context)

def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[0:3]
    context= {'product':product,'related_products':related_products}
    return render(request, 'store/detail.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total': 0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total': 0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("Item was Added", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        region=data['shipping']['region'],
        zipcode=data['shipping']['zipcode'],
    )
    return JsonResponse("Payment Complete",safe=False)