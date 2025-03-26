from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total
    context = {
        'cart_products':cart_products,
        'quantities':quantities,
        'totals':totals
    }
    return render(request, 'cart_summary.html', context)

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get Stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save the session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__() 

        # return response
        # response = JsonResponse({'Product Name:':product.name})
        response = JsonResponse({'qty':cart_quantity})
        messages.success(request, "Product Added To Cart....")
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        # Call delete function in cart
        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        messages.success(request, "Item Deleted From Shopping Cart....")
        return response
        

# def cart_update(request):
#     cart = Cart(request)
#     if request.POST.get('action') == 'post':
#         # Get Stuff
#         product_id = int(request.POST.get('product_id'))
#         product_qty = int(request.POST.get('product_qty'))
#         print("your quantity: -",product_qty)

#         cart.update(product=product_id, quantity=product_qty)
#         response = JsonResponse({'qty':product_qty})

#         return response
#         # return redirect('cart_summary')





from django.http import JsonResponse

def cart_update(request):
    cart = Cart(request)
    
    if request.method == 'POST' and request.POST.get('action') == 'post':
        # Get product ID and quantity from POST data
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        
        if not product_id or not product_qty:
            return JsonResponse({'error': 'Product ID or quantity is missing'}, status=400)

        try:
            product_id = int(product_id)
            product_qty = int(product_qty)
        except ValueError:
            return JsonResponse({'error': 'Invalid product ID or quantity'}, status=400)
        
        # Now update the cart with the product and quantity
        cart.update(product=product_id, quantity=product_qty)
        messages.success(request, "Your Cart Has Been Updated....")
        return JsonResponse({'qty': product_qty})

    return JsonResponse({'error': 'Invalid request'}, status=400)
