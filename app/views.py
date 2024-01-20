# from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q  #queue is for multiple filter conditions
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from .tokens import account_activation_token  
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage
from django.http import HttpResponseBadRequest
from django.utils.text import slugify
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist,ProductCategory,ProductVariation
from .forms import CustomerRegistrationForm,CustomerProfileForm,ProductVariationForm




# Create your views here.
# @login_required
def home(request):
    totalitem =0
    wishitem = 0
    product_categories = []  # Initialize with an empty list or another suitable default value
    #producthome=[]
    producthome= Product.objects.all()  # pylint: disable=E1101

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
        wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
        product_categories = ProductCategory.objects.all()  # pylint: disable=E1101
        # product_categories = ProductCategory.objects.all() # pylint: disable=E1101
    context={
        'totalitem':totalitem,
        'wishitem':wishitem,
        'product_categories':product_categories,
        'producthome':producthome,
    }
    return render(request,'home.html',context)



#@login_required
def about(request):
    totalitem =0
    wishitem = 0
    product_categories = ProductCategory.objects.all()  # pylint: disable=E1101

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
        wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101

    context={
        'totalitem':totalitem,
        'wishitem':wishitem,
        'product_categories':product_categories,
    }
    
    return render(request,'about.html',context)

#@login_required
def contact(request):
    totalitem =0
    wishitem = 0
    product_categories = ProductCategory.objects.all()  # pylint: disable=E1101

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
        wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
    context={
        'totalitem':totalitem,
        'wishitem':wishitem,
        'product_categories':product_categories,
    }
    return render(request,'contact.html',context)


# @method_decorator(login_required,name='dispatch')
# class Categoryview(View):
#     def get(self, request, val=None):  # Provide a default value for val
#         product = Product.objects.filter(category= val) # pylint: disable=E1101
#         title= Product.objects.filter(category=val).values('title') # pylint: disable=E1101
#         totalitem =0
#         wishitem = 0
#         if request.user.is_authenticated:
#             totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
#             wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101

#         context = {'product': product,
#                    'title':title,
#                    'totalitem':totalitem,
#                    'wishitem':wishitem,} # Pass the QuerySet as a dictionary
#         return render(request, 'category.html',context)



# Example in a view function



#CATEGORY 
#@method_decorator(login_required, name='dispatch')
class Categoryview(View):
    def get(self, request, val=None):
        totalitem = 0
        wishitem = 0

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
            

        product_categories = ProductCategory.objects.all()  # pylint: disable=E1101

        try:
            # Try to treat val as an integer (category ID)
            category_id = int(val)
            product = Product.objects.filter(category=category_id)
            title = Product.objects.filter(category=category_id).values('title')
        except ValueError:
            # If it's not an integer, treat it as a slug
            product = Product.objects.filter(category__slug=val)
            title = Product.objects.filter(category__slug=val).values('title')

        if not product.exists():
            raise Http404("Category does not exist")

        context = {
            'product': product,
            'title': title,
            'totalitem': totalitem,
            'wishitem': wishitem,
            'product_categories': product_categories,
        }

        return render(request, 'category.html', context)

# @method_decorator(login_required, name='dispatch')
# class Categoryview(View):
#     def get(self, request, val=None):
#         product_categories = ProductCategory.objects.all()  # Fetch all categories for reference
#         product = None
#         title = None

#         try:
#             # Try to convert val to an integer (assuming it's a numeric ID)
#             category_id = int(val)
#             product = Product.objects.filter(category=category_id)
#             title = Product.objects.filter(category=category_id).values('title')
#         except ValueError:
#             # If val is not a numeric ID, assume it's a category slug or name
#             category_name = slugify(val)  # Convert to a valid slug
#             product = Product.objects.filter(category__name=category_name)
#             title = Product.objects.filter(category__name=category_name).values('title')

#         totalitem = 0
#         wishitem = 0
#         if request.user.is_authenticated:
#             totalitem = len(Cart.objects.filter(user=request.user))
#             wishitem = len(Wishlist.objects.filter(user=request.user))

#         context = {
#             'product': product,
#             'title': title,
#             'totalitem': totalitem,
#             'wishitem': wishitem,
#             'product_categories': product_categories,
#         }
#         return render(request, 'category.html', context)

@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val) # pylint: disable=E1101
        title=Product.objects.filter(category=product[0].category).values('title') # pylint: disable=E1101
        totalitem =0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
            wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
            product_categories = ProductCategory.objects.all()  # pylint: disable=E1101

        context={'product':product,
                 'title':title,
                 'totalitem':totalitem,
                 'wishitem':wishitem,
                 'product_categories':product_categories,
                 }
        return render(request,'category.html',context)



# class ProductDetail(View):
#     @method_decorator(login_required)
#     def get(self,request,pk):
#         product = Product.objects.get(pk=pk) # pylint: disable=E1101
#         wishlist =Wishlist.objects.filter(Q(product=product)&Q(user =request.user))  # pylint: disable=E1101
#         totalitem =0
#         if request.user.is_authenticated:
#             totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
#         context = {'product': product,
#                    'totalitem':totalitem,
#                    'wishlist':wishlist,
#                    }
#         return render(request,'productdetail.html',context)  
@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        variations=[]
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
            product_categories = ProductCategory.objects.all()  # pylint: disable=E1101
            variations = ProductVariation.objects.filter(product=product)


        context = {
            'product': product,
            'totalitem': totalitem,
            'wishlist': wishlist,
            'wishitem':wishitem,
            'product_categories':product_categories,
            'variations':variations,
            
        }

        return render(request, 'productdetail.html', context)

# @method_decorator(login_required,name='dispatch')
# class CustomerRegistrationView(View):
#     def get(self, request):
#         form = CustomerRegistrationForm()
#         context = {'form': form}
#         return render(request, 'customerregistration.html', context)

#     def post(self, request):
#         form = CustomerRegistrationForm(request.POST)
#         context = {'form': form}

#         if form.is_valid():
#             # Custom validation for username
#             username = form.cleaned_data['username']
#             if any(char.isdigit() for char in username):
#                 form.add_error('username', "Username should only contain letters and no numbers.")
#                 messages.warning(request, "Invalid Input Data")
#                 return render(request, 'customerregistration.html', context)

#             form.save()
#             messages.success(request, "Congratulations! User Registered Successfully")
#             return redirect('login')  # Redirect to login page after successful registration
#         else:
#             messages.warning(request, "Invalid Input Data")

#         return render(request, 'customerregistration.html', context)



class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        context = {'form': form}
        return render(request, 'customerregistration.html', context)

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        context = {'form': form}

        if form.is_valid():
            # Custom validation for username
            username = form.cleaned_data['username']
            if any(char.isdigit() for char in username):
                form.add_error('username', "Username should only contain letters and no numbers.")
                messages.warning(request, "Invalid Input Data")
                return render(request, 'customerregistration.html', context)

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account on MySite'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            
            messages.success(request, "Please check your email to complete the registration.")
            return redirect('login')  # Redirect to login page after successful registration

        else:
            messages.warning(request, "Invalid Input Data")

        return render(request, 'customerregistration.html', context)


#for email otp authentication
def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
        return redirect("login")
    else:  
        return HttpResponse('Activation link is invalid!') 


    



@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        totalitem =0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
            wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
            product_categories = ProductCategory.objects.all()  # pylint: disable=E1101


        form =CustomerProfileForm()
        context ={ 'form':form,
                  'totalitem':totalitem,
                  'product_categories':product_categories,
                  'wishitem':wishitem,}
        return render(request,'profile.html',context)
    
    def post(self,request):
        form =CustomerProfileForm(request.POST)
        totalitem =0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
            wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
            product_categories = ProductCategory.objects.all()  # pylint: disable=E1101


        context ={ 'form':form,
                  'totalitem':totalitem,
                  'wishitem':wishitem,
                  'product_categories':product_categories,}

        
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            
            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,pincode=pincode)
            reg.save()
            messages.success(request,"Congratulations !! Profile Saved Successfully ")
        else:
            messages.warning(request,"Invalid Input Data")
            
        return render(request,'profile.html',context)
                            
@login_required  
def address(request):
    add=Customer.objects.filter(user=request.user) # pylint: disable=E1101
    totalitem =0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
        wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
        product_categories = ProductCategory.objects.all()  # pylint: disable=E1101

    context={
        'add': add,
         'totalitem':totalitem,
         'wishitem':wishitem,
         'product_categories':product_categories,
    }
    return render(request,'address.html',context)
    
@method_decorator(login_required,name='dispatch')   
class updateAddress(View):
    def get(self,request,pk):
        totalitem =0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
            wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
            product_categories = ProductCategory.objects.all()  # pylint: disable=E1101

        add = Customer.objects.get(pk=pk)  # pylint: disable=E1101
        form =CustomerProfileForm( instance=add)
        context ={ 'form':form,
                    'totalitem':totalitem,
                    'wishitem':wishitem,
                    'product_categories':product_categories,
                  }
        return render(request,'updateaddress.html',context)
    def post(self,request,pk):
        form =CustomerProfileForm(request.POST)
        
        if form.is_valid():
            add = Customer.objects.get(pk=pk)  # pylint: disable=E1101
            add.name=form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.pincode=form.cleaned_data['pincode']
            add.save()
            messages.success(request,"Congratulation ! Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
            
        
        return redirect('address')
    
    
# @login_required    
# def add_to_cart(request):
#     user = request.user
#     product_id = request.GET.get('prod_id')
#     product = Product.objects.get(id=product_id)  # pylint: disable=E1101
#     Cart(user=user,product=product).save()
#     return redirect('/cart')
    
    
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)  # pylint: disable=E1101

    # Check if the product is already in the cart
    cart_item = Cart.objects.filter(user=user, product=product).first()  # pylint: disable=E1101

    if cart_item:
        # If the product is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If the product is not in the cart, create a new entry
        Cart(user=user, product=product).save()

    return redirect('/cart') 
    
    
    
@login_required  
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    totalamount = 0
    stock_unavailable = False  # Flag to check if stock is unavailable

    # Fetch variation details from the request
    selected_quantity = request.GET.get('selected_quantity', '')  # Change as per your actual input names
    selected_price = request.GET.get('selected_price', '')
    selected_discounted_price = request.GET.get('selected_discounted_price', '')

    for cart_item in cart:
        product = cart_item.product

        # Check if the selected quantity exceeds available stock
        if cart_item.quantity > product.stock_quantity:
            stock_unavailable = True
            cart_item.quantity = product.stock_quantity  # Set quantity to available stock

        # Calculate total amount
        amount += cart_item.quantity * product.discounted_price
        totalamount = amount + 40  # Shipping charge hardcoded to 40 (change based on location)

        # Update the available stock for the product
        # product.stock_quantity -= cart_item.quantity
        # product.save()

    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
        product_categories = ProductCategory.objects.all()

    context = {
        'cart': cart,
        'selected_quantity': selected_quantity,
        'selected_price': selected_price,
        'selected_discounted_price': selected_discounted_price,
        'amount': amount,
        'totalamount': totalamount,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'product_categories': product_categories,
        'stock_unavailable': stock_unavailable,  # Pass the flag to the template
    }

    return render(request, 'addtocart.html', context)

    
    
    
    
    
    
# @login_required  
# def show_cart(request):
#     user = request.user
#     cart = Cart.objects.filter(user=user)
#     amount = 0
#     value = 0
#     totalamount = 0
#     stock_unavailable = False  # Flag to check if stock is unavailable

#     for cart_item in cart:
#         product = cart_item.product

#         # Check if the selected quantity exceeds available stock
#         if cart_item.quantity > product.stock_quantity:
#             stock_unavailable = True
#             cart_item.quantity = product.stock_quantity  # Set quantity to available stock

#         value = cart_item.quantity * product.discounted_price
#         amount += value
#         totalamount = amount + 40  # Shipping charge hardcoded to 40 (change based on location)

#         # Update the available stock for the product
#         # product.stock_quantity -= cart_item.quantity
#         # product.save()

#     totalitem = 0
#     wishitem = 0

#     if request.user.is_authenticated:
#         totalitem = len(Cart.objects.filter(user=request.user))
#         wishitem = len(Wishlist.objects.filter(user=request.user))
#         product_categories = ProductCategory.objects.all()

#     context = {
#         'cart': cart,
#         'value': value,
#         'amount': amount,
#         'totalamount': totalamount,
#         'totalitem': totalitem,
#         'wishitem': wishitem,
#         'product_categories': product_categories,
#         'stock_unavailable': stock_unavailable,  # Pass the flag to the template
#     }

#     return render(request, 'addtocart.html', context)



# def show_cart(request):
#     user = request.user
#     cart = Cart.objects.filter(user=user)  # pylint: disable=E1101
#     amount =0
#     value=0
#     totalamount=0
    
  
#     for p in cart:
#         value = p.quantity * p.product.discounted_price
#         amount = amount + value
#         totalamount = amount + 40    #shipping charge hardcore to 40 change on location basis
    
#     totalitem =0
#     wishitem = 0
#     if request.user.is_authenticated:
#         totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
#         wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
#         product_categories = ProductCategory.objects.all()  # pylint: disable=E1101
        
 
#     context={
#         'cart': cart,
#         'value':value,
#         'amount':amount,
#         'totalamount':totalamount,
#         'totalitem':totalitem,
#         'wishitem':wishitem,
#         'product_categories':product_categories,
       
      
        
#     }
    
#     return render(request,'addtocart.html',context)






@login_required
def show_wishlist(request):
    user = request.user
    totalitem =0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
        wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
        product_categories = ProductCategory.objects.all()  # pylint: disable=E1101

    product = Wishlist.objects.filter(user=user) # pylint: disable=E1101
    context ={
        'totalitem':totalitem,
        'wishitem':wishitem,
        'product':product,
        'product_categories':product_categories,
        
    }
    return render(request,'wishlist.html',context)



@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        user=request.user
        add = Customer.objects.filter(user=user)   # pylint: disable=E1101
        cart_items = Cart.objects.filter(user=user)  # pylint: disable=E1101
        famount = 0
        totalitem =0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user)) # pylint: disable=E1101
            wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
            product_categories = ProductCategory.objects.all()  # pylint: disable=E1101


        for p in cart_items:
            value  = p.quantity * p.product.discounted_price
            famount = famount + value
            totalamount = famount + 40  #shipping cost
            razoramount =int(totalamount * 100)
            client = razorpay.Client(auth =(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
            data  ={"amount":razoramount, "currency" :"INR", "receipt":"order_rcptid_11"}
            payment_response = client.order.create(data=data)  # pylint: disable=E1101
            print(payment_response)
            order_id = payment_response['id']
            order_status = payment_response['status']
            if order_status == 'created':
                payment =Payment(
                    user=user,
                    amount=totalamount,
                    razorpay_order_id = order_id,
                    razorpay_payment_status = order_status,
                )
                payment.save()
                # Reduce stock quantity for each product in the cart
                product = p.product
                product.stock_quantity -= p.quantity
                product.save()
                    
            print(add.values())
            
        context={
            'add':add,
            'cart_items':cart_items,
            'totalamount':totalamount,
            'razoramount':razoramount,
            'client':client,
            'data':data,
            'payment_response':payment_response,
            'order_id':order_id,
            'order_status':order_status,
            'totalitem':totalitem,
            'wishitem':wishitem,
            'product_categories':product_categories,
        }
        return render(request,'checkout.html',context)
        


@login_required
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    # print("Payment_done :oid =  ")
    user=request.user
    # return redirect("orders")
    customer=Customer.objects.get(id=cust_id)  # pylint: disable=E1101
    # To update payment status and payment id
    payment =Payment.objects.get(razorpay_order_id=order_id) # pylint: disable=E1101
    payment.paid=True
    payment.razorpay_order_id=payment_id
    payment.save()
    
    # To save order details
    
    cart =Cart.objects.filter(user=user)  # pylint: disable=E1101
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    #messages.success(request, 'Your order was successfully placed!')
    return redirect("orders")
    # return redirect('payment_done/?order_id=your_order_id&payment_id=your_payment_id&cust_id=your_cust_id')



# def payment_done(request):
#     order_id = request.GET.get('order_id')
#     payment_id = request.GET.get('payment_id')
#     cust_id = request.GET.get('cust_id')

#     # Check if cust_id is not empty
#     if cust_id:
#         try:
#             # Attempt to retrieve the Customer object
#             customer = Customer.objects.get(id=cust_id)
#         except Customer.DoesNotExist:
#             # Handle the case where Customer is not found
#             return HttpResponse("Invalid Customer ID")

#         # To update payment status and payment id
#         payment = Payment.objects.get(razorpay_order_id=order_id)
#         payment.paid = True
#         payment.razorpay_order_id = payment_id
#         payment.save()

#         # To save order details
#         cart = Cart.objects.filter(user=request.user)
#         for c in cart:
#             OrderPlaced(user=request.user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
#             c.delete()

#         return redirect(f'/orders/?cust_id={cust_id}')
#     else:
#         # Handle the case where cust_id is None or empty string
#         return HttpResponse("Invalid request")


@login_required 
def orders(request):
    totalitem =0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))  # pylint: disable=E1101
        wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
        product_categories = ProductCategory.objects.all()  # pylint: disable=E1101


    order_placed =OrderPlaced.objects.filter(user=request.user)  # pylint: disable=E1101
    # customer = Customer.objects.filter(user=request.user)# pylint: disable=E1101
    customer = Customer.objects.filter(user=request.user).first()  # pylint: disable=E1101
    
    context={
        'order_placed':order_placed,
        'totalitem':totalitem,
        'customer':customer,
        'wishitem':wishitem,
        'product_categories':product_categories,
        
        
    }
    return render(request,'orders.html',context)
    
    
    
    
# def orders(request):
#     totalitem = 0
#     wishitem = 0
#     if request.user.is_authenticated:
#         totalitem = len(Cart.objects.filter(user=request.user))
#         wishitem = len(Wishlist.objects.filter(user=request.user))
#         product_categories = ProductCategory.objects.all()

#     # Retrieve cust_id from the GET parameters
#     cust_id = request.GET.get('cust_id')

#     order_placed = OrderPlaced.objects.filter(user=request.user)
#     customer = Customer.objects.filter(user=request.user, id=cust_id).first()

#     context = {
#         'order_placed': order_placed,
#         'totalitem': totalitem,
#         'customer': customer,
#         'wishitem': wishitem,
#         'product_categories': product_categories,
#     }
#     return render(request, 'orders.html', context)


#

#For Searchbox in the navbar 
@login_required
def search(request):
    query = request.GET['search']
    totalitem =0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))  # pylint: disable=E1101
        wishitem = len(Wishlist.objects.filter(user=request.user)) # pylint: disable=E1101
        product_categories = ProductCategory.objects.all()  # pylint: disable=E1101

 
    product =Product.objects.filter(Q(title__icontains =query))
    context ={
        'product':product,
        'totalitem':totalitem,
        'wishitem':wishitem,
        'product_categories':product_categories,
        
    }

    return render(request,'search.html',context)
@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) # pylint: disable=E1101
        c.quantity+=1
        c.save()
        user = request.user
        cart=Cart.objects.filter(user=user)   # pylint: disable=E1101
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount+value
            totalamount = amount + 40  #shipping charge hardcore to 40 change on location basis
        
        
        data ={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount' :totalamount
            
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))  # pylint: disable=E1101

        # Prevent quantity from going below one
        if c.quantity > 1:
            c.quantity -= 1
            c.save()

        user = request.user
        cart = Cart.objects.filter(user=user)  # pylint: disable=E1101
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
            totalamount = amount + 40  # shipping charge hardcoded to 40, change on location basis

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)
    
# @login_required    
# def remove_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET['prod_id']
#         c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) # pylint: disable=E1101

#         c.delete()
#         user = request.user
#         cart=Cart.objects.filter(user=user)   # pylint: disable=E1101
#         amount = 0
#         for p in cart:
#             value = p.quantity * p.product.discounted_price
#             amount = amount+value
#             totalamount = amount + 40  #shipping charge hardcore to 40 change on location basis
        
        
#         data ={
#             'quantity':c.quantity,
#             'amount': amount,
#             'totalamount' :totalamount
            
#         }
#         return JsonResponse(data)
@login_required    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        try:
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=user))
            cart_item.delete()
        except Cart.DoesNotExist:
            # Handle the case where the cart item doesn't exist
            pass

        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value

        totalamount = amount + 40  # Shipping charge hardcoded to 40, change on location basis

        data = {
            'quantity': 0,  # Set quantity to 0 since the item is removed
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


#adding the product to wishlist
@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)  # pylint: disable=E1101
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'Added to Wishlist'
        }
        return JsonResponse(data)

#removing the product from the wishlist
@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)  # pylint: disable=E1101
        user = request.user

        # Check if the Wishlist object exists before attempting to delete
        wishlist_entry = Wishlist.objects.filter(user=user, product=product).first()  # pylint: disable=E1101
        if wishlist_entry:
            wishlist_entry.delete()

        data = {
            'message': 'Removed from Wishlist'
        }
        return JsonResponse(data)




