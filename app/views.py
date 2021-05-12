from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlcaed
from django.contrib.auth.models import User
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages

from django.db.models import Q
from django.http import JsonResponse

# this used to prevent access page while user is not logged in but only for function based view 
from django.contrib.auth.decorators import login_required

# this used to prevent access page while user is not logged in but only for class based view 
from django.utils.decorators import method_decorator

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

@login_required
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

@login_required
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

@login_required
def buy_now(request):
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
    return redirect('/checkout')


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op = OrderPlcaed.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order':op})


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


# this id how we impliment login_required in class absed view 
@method_decorator(login_required,name='dispatch')
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
            email = form.cleaned_data['email']
            c = User.objects.filter(email=email).exists()
            if c:
                messages.warning(request,'Email Already Exists')
            else:
                form.save()
                messages.success(request,'Congratulations!! Registered Successfully')
        return render(request, 'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount =0.0
    shipping_amount =40.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for i in cart_product:
            temp = (i.quantity * i.product.discounted_price)
            amount +=temp
    total_amount = amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'tamt':total_amount,'cart_items':cart_items})

@login_required
def paymentdone(request):
    if request.method == 'GET':
        user = request.user
        custid= request.GET.get('custid')
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlcaed(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
            c.delete()
        return redirect("orders")