from django.shortcuts import render ,redirect,HttpResponseRedirect
from shop.models.customer import Customer
from django.contrib.auth.hashers import check_password
from django.views import View

class Login(View):
    return_url = None
    def get(self,request):
        Login.return_url = request.GET.get('return_url')
        return render(request,'login.html')
    def post(self,request):
        postData = request.POST
        email = postData.get('email')
        value = {
            'email':email
        }
        data = {}
        
        password = postData.get('password')
        customer = Customer.customer_by_email(email)
        error_msg = None
        if customer:
            flag  = check_password(password, customer.password)
            if flag:
                request.session["customer"] = customer.id
                request.session["first_name"] = customer.first_name
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    return redirect('index')
            else:
                error_msg = "Email or password is wrong!!"
                
        else:
            error_msg = "Email or password wrong!!!"
        data['values'] = value
        data['error'] = error_msg
        return render(request,'login.html',data)
