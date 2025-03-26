from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart
from payment.models import ShippingAddress
from payment.forms import ShoppingForm
# Create your views here.

def search(request):
    # Datemine if they filled out the form
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # Test for null
        if not searched:
            messages.success(request, "That Product does not Exist... Please try Again.")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})


def update_info(request):
    if request.user.is_authenticated:
        # Get current user
        current_users = Profile.objects.get(user__id=request.user.id)
        # Get current user shopping info
        shopping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #  Get original user form
        form = UserInfoForm(request.POST or None, instance=current_users)
        # Get user shopping form
        shipping_form = ShoppingForm(request.POST or None, instance=shopping_user)

        if form.is_valid() or shipping_form.is_valid():
            #  save original form
            form.save()
            # save shipping form
            shipping_form.save()
            messages.success(request, "User Info Has Been Updated!!")
            return redirect('home')
        context = {
            'form':form,
            'shipping_form':shipping_form
            }
        return render(request, "update_info.html", context)
        
    else:
        messages.success(request, "User Must Be Logged In To Access That Page!!")
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password Has Been Updated....")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})
    else:
        messages.success(request, "User Must Be Logged In To Access That Page!!")
        return redirect('home')



def update_user(request):
    if request.user.is_authenticated:
        current_users = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_users)
        
        if user_form.is_valid():
            user_form.save()
            login(request, current_users)
            messages.success(request, "User Profile Has Been Updated!!")
            return redirect('home')
        
        return render(request, "update_user.html", {'user_form':user_form})
    
    else:
        messages.success(request, "User Must Be Logged In To Access That Page!!")
        return redirect('home')



def category_summary(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, "category_summary.html", context)


def category(request, foo):
    # Replace Hyphens with space
    foo = foo.replace('-', ' ')
    
    #  grab the category from url
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        
        context = {
            'category':category,
            'products':products,
        }
        return render(request, "category.html", context)
    except:
        messages.success(request, "Thar Category Doenot Exists!")
        return redirect('home')

    

def product(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product':product,
    }
    return render(request, "product.html", context)



def home(request):
    products = Product.objects.all()
    context = {
        'products':products,
    }
    return render(request, "home.html", context)


def about(request):
    return render(request, "about.html")


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # DO some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # get their sae cart from database
            save_cart = current_user.old_cart
            # convert database string to python dictionary
            if save_cart:
                # convert to dictionary using json
                conveted_cart = json.loads(save_cart)
                # Add to loaded cart dictionary to our session
                # get the cart
                cart = Cart(request)
                # loop thru the cart and add the items from database
                for key,value in conveted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, "You Have Been Logged In..")
            return redirect('home')
        else:
            messages.success(request, "There was an error, please Try again...")
            return redirect('login')
    else:
        return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged Out.....")
    return redirect('home')


def register_user(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Username Created - Please Fill Out Your Info Below....")
            return redirect('update_info')
        else:
            messages.success(request, "There was a problem Registring, please try again...")
            return redirect('register')
    else:
        return render(request, "register.html",{'form':form})



