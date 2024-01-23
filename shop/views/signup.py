from django.shortcuts import render ,redirect
from shop.models.customer import Customer
from django.contrib.auth.hashers import make_password
from django.views import View
class Signup(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        PostData = request.POST
        first_name = PostData.get('firstname')
        phone = PostData.get('phone')
        email = PostData.get('email')
        password = PostData.get('password')
        value = {
            'first_name' : first_name,
            'phone' : phone,
            'email' : email
        }
        password = make_password(password)
        customer = Customer(first_name = first_name,
                                phone = phone,
                                email = email,
                                password = password)
        error_msg = self.validate(customer)
    
        if not error_msg:
            customer.register()
            request.session["customer"] = customer.id
            request.session["first_name"] = customer.first_name
            return redirect('index')
        else:
            data = {
                'error' : error_msg,
                'values' : value
            }
            return render(request,'signup.html',data)
    def validate(self,customer):
        error_msg = None
        if not customer.first_name:
            error_msg = 'Please enter first name:)'
        elif len(customer.first_name) < 2:
            error_msg = 'Name lenght must be minimum 4 character :)'
        isExist = customer.isExist()
        if isExist:
            error_msg = "email Already Registered"
        return error_msg
