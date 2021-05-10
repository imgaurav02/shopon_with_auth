from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlcaed
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages

from django.db.models import Q
from django.http import JsonResponse
# def home(request):
#  return render(request, 'app/home.html')
# class based views defining

class ProductView(View):
    def get(Self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request,'app/home.html', {'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})

class ProdcutDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',{'product':product})

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    c= Cart.objects.filter(product=product_id,user=user).exists()
    if c:
        update = Cart.objects.get(Q(product=product_id) & Q(user = request.user))
        print(update)
        update.quantity +=1
        update.save()
    else:
        product = Product.objects.get(id=product_id)
        Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user= user)
        amount =0.0
        shipping_amount =40.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for i in cart_product:
                temp = (i.quantity * i.product.discounted_price)
                amount +=temp
        else:
            return render(request,'app/empty_cart.html')
        total_amount = amount+shipping_amount
        return render(request, 'app/addtocart.html',{'carts':cart,'amount':amount,'total_amount':total_amount})
        
def plus_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity +=1
        c.save()
        amount =0.0
        shipping_amount =40.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        if cart_product:
            for i in cart_product:
                temp = (i.quantity * i.product.discounted_price)
                amount +=temp
        total_amount = amount+shipping_amount

        data = {
            'quantity' : c.quantity,
            'amount':amount,
            'totalamount':total_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity =c.quantity-1
        c.save()
        amount =0.0
        shipping_amount =40.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        if cart_product:
            for i in cart_product:
                temp = (i.quantity * i.product.discounted_price)
                amount +=temp
        total_amount = amount+shipping_amount

        data = {
            'quantity' : c.quantity,
            'amount':amount,
            'totalamount':total_amount
        }
        return JsonResponse(data)
def remove_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.delete()
        amount =0.0
        shipping_amount =40.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        if cart_product:
            for i in cart_product:
                temp = (i.quantity * i.product.discounted_price)
                amount +=temp
        total_amount = amount+shipping_amount

        data = {
            'amount':amount,
            'totalamount':total_amount
        }
        return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        # saving form using cleaned data method 
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            phone = form.cleaned_data['phone']
            usr = request.user
            reg = Customer(user=usr,name=name,city=city,locality=locality,state=state,zipcode=zipcode,phone=phone)
            reg.save()
            messages.success(request,'Address Added SuccessFully!!')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
        

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')


def mobile(request,data = None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below' :
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above' :
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

# we are using default login so defining direct in urls not done anything in views 

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations!! Registered Successfully')
        return render(request, 'app/customerregistration.html',{'form':form})


def checkout(request):
 return render(request, 'app/checkout.html')
