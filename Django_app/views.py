from django.contrib import messages
from django.shortcuts import render,redirect
from django.db import models
from django.contrib.auth.models import User
from .models import Category, Customer, Order, OrderItem,Products2,ContactUs, ShippingAddress, UserProfile
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
import json
import uuid
import datetime
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.mail import message, send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    dests = Products2.objects.filter(category__name='Popular')
    dests2 = Products2.objects.filter(category__name='Premium')
    return render(request,'index.html',{'dests':dests,'cardItems':cartItems,'dests2':dests2})

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact = ContactUs(Name=name,Email=email,Subject=subject,Message=message)
        contact.save();
        messages.success(request,'Message sent successfully')

    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})
    # customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    return render(request,'contact.html',{'cardItems':cartItems})


def products(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})
    search = ""
    if request.GET.get('search'):
        search = request.GET.get('search')
    dests = Products2.objects.filter(Product_name__icontains=search).order_by('?')
    # customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    page = request.GET.get('page')
    results = 21
    paginator = Paginator(dests, results)
    try:
        dests = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        dests = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        dests = paginator.page(page)
    return render(request,'products.html',{'dests':dests,'cardItems':cartItems,'paginator':paginator})


def register(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})
    # customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.success(request,'*Username is already taken','success')
            return redirect('/register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'This email already exists')
            return redirect('/register')
        elif password != confirmpassword:
            messages.info(request,'Passwords does not match')
            return redirect('/register')
        else:
            user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password,email=email)
            user.save();
            template = render_to_string('email.html', {'name':first_name})
            subject = 'Your Account is Registered!'
            send_mail(
                subject,
                template,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('/login')
        
    return render(request,'register.html',{'cardItems':cartItems})
        

def loginUser(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})
    # customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/userprofile')
        else:
            messages.info(request,'Incorrect username or password') 
            return render(request,'login.html')

    return render(request,'login.html',{'cardItems':cartItems})


def logoutUser(request):
    logout(request)
    return redirect('/')

# @login_required(login_url='login')
def userprofile(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})
    if request.user.is_anonymous:
        messages.info(request,'You need to Login first') 
        return redirect('/login')
    
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    ok, created = UserProfile.objects.get_or_create(user=request.user,
    defaults={'Address':'','City':'','PostalCode':0,'PhoneNo':0})
    cartItems = order.get_cart_items
    return render(request,'userprofile.html',{'ok':ok,'cardItems':cartItems})

def useraddress(request):
    return render(request,'useraddress.html')

def cart(request):
    if request.user.is_anonymous:
        messages.info(request,'You need to Login first') 
        return redirect('/login')
    else:
        # customer, created = Customer.objects.get_or_create(user=request.user,name=request.user.username,email=request.user.email)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        return render(request,'cart.html',{'items':items,'order':order,'cardItems':cartItems})

def checkout(request):

    ok = request.user.userprofile
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})


    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    # return render(request,'cart.html',{})
    context = {'ok':ok,'items':items,'order':order,'cardItems':cartItems}
    return render(request,'checkout.html',context)

def addaddress(request):

    if request.method == 'POST':
        # user, created = UserProfile.objects.get_or_create(user=request.user)
        # ok = request.user.userprofile
        Address = request.POST.get('address')
        City = request.POST.get('city')
        PhoneNo = request.POST.get('contactno')
        PostalCode = request.POST.get('postalcode')
        userprofilee= UserProfile(Address=Address,City=City,PhoneNo=PhoneNo,PostalCode=PostalCode,user_id=request.user.id)
        userprofilee.save();
        
        return redirect('/userprofile')
    return render(request, 'useraddress.html')

def editaddress(request):
    ok = request.user.userprofile

    if request.method == 'POST':
        
        # user, created = UserProfile.objects.get_or_create(user=request.user)
        # ok = request.user.userprofile
        with connection.cursor() as cursor:
            dicto = {
            "Address" : request.POST.get('address'),
            "City" : request.POST.get('city'),
            "PhoneNo" : request.POST.get('contactno'),
            "PostalCode" : request.POST.get('postalcode'),
            "idd" : request.user.id
            }
        # userprofilee= UserProfile(Address=Address,City=City,PhoneNo=PhoneNo,PostalCode=PostalCode)
        # userprofilee.save();
        # with connection.cursor() as cursor:
            cursor.execute("UPDATE `django_app_userprofile` SET Address = '%(Address)s', City = '%(City)s', PostalCode = '%(PostalCode)s',  PhoneNo = '%(PhoneNo)s' WHERE `django_app_userprofile`.`user_id` = '%(idd)s'" % dicto);
        #     row = cursor.fetchall()
        # return row
        return redirect('/userprofile')
    
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    return render(request, 'editaddress.html',{'ok':ok,'cardItems':cartItems})


def editaddress2(request):
    ok = request.user.userprofile

    if request.method == 'POST':
        # user, created = UserProfile.objects.get_or_create(user=request.user)
        # ok = request.user.userprofile
        with connection.cursor() as cursor:
            dicto = {
            "Address" : request.POST.get('address'),
            "City" : request.POST.get('city'),
            "PhoneNo" : request.POST.get('contactno'),
            "PostalCode" : request.POST.get('postalcode'),
            "idd" : request.user.id
            }
        # userprofilee= UserProfile(Address=Address,City=City,PhoneNo=PhoneNo,PostalCode=PostalCode)
        # userprofilee.save();
        # with connection.cursor() as cursor:
            cursor.execute("UPDATE `django_app_userprofile` SET Address = '%(Address)s', City = '%(City)s', PostalCode = '%(PostalCode)s',  PhoneNo = '%(PhoneNo)s' WHERE `django_app_userprofile`.`user_id` = '%(idd)s'" % dicto);
        #     row = cursor.fetchall()
        # return row
        return redirect('/checkout')

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    return render(request, 'editaddress2.html',{'ok':ok,'cardItems':cartItems})

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('ProductId:', productId)
    print('Action:', action)

    # customer, created = Customer.objects.get_or_create(user=request.user,name=request.user.username,email=request.user.email)
    customer = request.user.customer
    product = Products2.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product2=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        messages.success(request,'Successfully added to cart')
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        messages.success(request,'Item removed from cart')

    orderItem.save()


    if orderItem.quantity <= 0:
        orderItem.delete()

   


    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    total = data['form']['total']
    order.transaction_id = transaction_id

    # if total == order.get_cart_total:
    order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer = customer,
        order = order,
        address = data['shipping']['address'],
        city = data['shipping']['city'],
        phoneNo = data['shipping']['phoneNo'],
        postalCode = data['shipping']['zipCode'],
    )
    messages.info(request,'Order Placed Successfully')

    return JsonResponse('payment Submitted...',safe=False)


def viewProduct(request, id):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})
    product = Products2.objects.get(id=id)
    # customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    similar = Products2.objects.filter(category__name='Shoes').exclude(id=id).order_by('?')
    similar1 = Products2.objects.filter(category__name='Bags').exclude(id=id).order_by('?')
    similar2 = Products2.objects.all().order_by('?')
   
    context = {'product':product, 'cardItems':cartItems,'similar':similar,'similar1':similar1,'similar2':similar2}


    return render(request,'viewproduct.html',context)


def ok(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    dests = Products2.objects.filter(category__name='Bags')
    page = request.GET.get('page')
    results = 15
    paginator = Paginator(dests, results)
    try:
        dests = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        dests = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        dests = paginator.page(page)
    return render(request,'products.html',{'dests':dests,'cardItems':cartItems,'paginator':paginator})

def ok2(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    dests = Products2.objects.filter(category__name='Shoes')
    page = request.GET.get('page')
    results = 15
    paginator = Paginator(dests, results)
    try:
        dests = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        dests = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        dests = paginator.page(page)
    return render(request,'products.html',{'dests':dests,'cardItems':cartItems,'paginator':paginator})

def ok3(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    dests = Products2.objects.filter(category__name='Belt')
    page = request.GET.get('page')
    results = 15
    paginator = Paginator(dests, results)
    try:
        dests = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        dests = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        dests = paginator.page(page)
    return render(request,'products.html',{'dests':dests,'cardItems':cartItems,'paginator':paginator})

def ok4(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    dests = Products2.objects.filter(category__name='Wallet')
    page = request.GET.get('page')
    results = 15
    paginator = Paginator(dests, results)
    try:
        dests = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        dests = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        dests = paginator.page(page)
    return render(request,'products.html',{'dests':dests,'cardItems':cartItems,'paginator':paginator})

def ok5(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user,
        defaults={'name':request.user.username,'email':request.user.email})
    else:
        customer, created = Customer.objects.get_or_create(user_id=2,
        defaults={'name':'anonymous','email':'email'})
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    dests = Products2.objects.filter(category__name='Watch')
    page = request.GET.get('page')
    results = 15
    paginator = Paginator(dests, results)
    try:
        dests = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        dests = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        dests = paginator.page(page)
    return render(request,'products.html',{'dests':dests,'cardItems':cartItems,'paginator':paginator})

def sai(request):
    return render(request,'ok.html')
