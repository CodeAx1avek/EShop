from django.shortcuts import render ,redirect
from shop.models.product import Product
from shop.models.category import Category
from django.views import View
from django.db.models import Q
class Index(View):
    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
                quantity = cart.get(product)    
                if quantity:
                       if remove:
                           if quantity <= 1:
                                cart.pop(product)
                           else:
                                cart[product] = quantity - 1
                       else:
                            cart[product] = quantity + 1
                    
                else:
                    cart[product] = 1

        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] =  cart
        return redirect('index')
        

    
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
             request.session['cart'] = {}
        products = None
        user = request.session.get('first_name')
        categories = Category.get_category()
        CategoryID = request.GET.get('category')
        search_query = ''
        if CategoryID:
            products= Product.get_category_by_id(CategoryID)
        elif request.GET.get('q'):
            search_query = request.GET.get('q')
            products = Product.objects.filter(Q(name__icontains = search_query))
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
        data['username'] = user
        return render(request,'index.html',data) 



    

    
def logout(request):
    request.session.clear()
    return redirect('index')
            