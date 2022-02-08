from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from app.models import Customer, Product, Cart, OrderPlaced
from app.forms import CustomerRegistrationform, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views



# Create your views here.


class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'home.html', {'topwears':topwears,'bottomwears':bottomwears, 'mobiles':mobiles})

       

def product_detail(request):
    return render(request,'productdetail.html')


class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'productdetail.html', {'product':product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product_id).save()
    print(product)
    return render('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount

            return render(request, 'addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
    else: 
        return render(request,'emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount= 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount= 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.delete()
        amount= 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount

        data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
        return JsonResponse(data)




def buy_now(request):
    return render(request,'buynow.html')

def profile(request):
    return render(request,'profile.html')
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'address.html',{'add':add, 'active':'btn-primary'})

    
@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request,'orders.html',{'order_placed':op})



def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data =='Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)

    return render(request,'mobile.html', {'mobiles':mobiles})

def login(request):
    return render(request,'login.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationform()
        return render(request,'Customerregistration.html',{'form':form})
    def post(self, request):
        form = CustomerRegistrationView(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return  render(request,'Customerregistration.html',{'form':form})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
      form = CustomerProfileForm()
      return render(request,'profile.html',{'form':form,
      'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,
            state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulation!! Profile Updated successfully')
            return render(request,'profile.html',{'form':form,'active':'btn-primary'})
    
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
      for p in cart_product: 
          tempamount = (p.quantity * p.product.discounted_price )
          amount += tempamount
          totalamount = amount + shipping_amount


    return render(request, 'checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})



def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, 
        product=c.product , quantity=c.quantity).save()
        c.delete()
        return redirect("orders")
