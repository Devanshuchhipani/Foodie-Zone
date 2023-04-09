from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import login, authenticate, logout, get_user_model 
from Foodie_Zone.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import json

count=3
b1 = 1
re = 0
# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def menu(request):
    context={}
    
    item1 = Items.objects.filter( Rest_id = 'R001001')
    item2 = Items.objects.filter( Rest_id = 'R002001')
    item3 = Items.objects.filter( Rest_id = 'R003001')
    item4 = Items.objects.filter( Rest_id = 'R004001')

    context['item1'] = item1
    context['item2'] = item2
    context['item3'] = item3
    context['item4'] = item4
    #print(context)
    return render(request,'menu.html',context)

def partner(request):
    context={}
    members = Partner.objects.all().order_by('name')
    context['partner_members'] = members
    print(context)
    return render(request,'partner.html',context)

def contact_us(request):
    context={}
    if request.method=="POST":
        name = request.POST.get("name")
        em = request.POST.get("email")
        sub = request.POST.get("subject")
        msz = request.POST.get("message")
        
        obj = Contact(name=name, email=em, subject=sub, message=msz)
        obj.save()
        context['message']=f"Dear {name}, Thanks for your time!"

    return render(request,'contact.html', context)

def register(request):
    context={}
    if request.method=="POST":
        #fetch data from html form
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        contact = request.POST.get('number')

         
        check = User.objects.filter(username=email)
        if len(check)==0:
            #Save data to both tables
            usr = User.objects.create_user(email, email, password)
            usr.first_name = name
            usr.save()
            
            global count
            
            def increment():
                global count
                count = count + 1
            
            increment()
            print(count)
            cus = f'C00000{count}'
            profile = Customer(user=usr, customer_id = cus ,customer_name = name ,mobile_no = contact)
            profile.save()
            context['status'] = f"User {name} Registered Successfully!"
        else:
            context['error'] = f"A User with this email already exists"

    return render(request,'register.html',context)

def check_user_exists(request):
    email = request.GET.get('usern')
    check = User.objects.filter(username=email)
    if len(check)==0:
        return JsonResponse({'status':0,'message':'Not Exist'})
    else:
        return JsonResponse({'status':1,'message':'A user with this email already exists!'})

def signin(request):
    context={}
    if request.method=="POST":
        email1 = request.POST.get('email')
        passw = request.POST.get('password')

        check_user = authenticate(username=email1, password=passw)
        
        # print(check_user)
        # login_user = get_object_or_404(User,email = email1)
        # profile = User.objects.get(email = email1)
        # print(profile)
        
        usr = get_user_model()

        try:
            def_user_id = usr.objects.get(email = email1).id
        except usr.DoesNotExist:
            context['message'] = f"user does not exist"
            return render(request,'login.html',context) 
        print(def_user_id)

        u1 = Customer.objects.filter(user_id = def_user_id )
        print(u1)

        u2 = Restaurant.objects.filter(user_id = def_user_id )
        print(u2)

        if check_user:
             login(request, check_user)
             if check_user.is_superuser or check_user.is_staff:
                 return HttpResponseRedirect('/admin')
             elif u1:
                 return HttpResponseRedirect('/dashboard2')
             else:
                 return HttpResponseRedirect('/dashboard1')
        else:
             context.update({'message':'Invalid Login Details!','class':'alert-danger'})

    return render(request,'login.html',context)

def dashboard1(request):
    context={}
    login_user = get_object_or_404(User, id = request.user.id)
    #fetch login user's details
    profile = Restaurant.objects.get(user__id=request.user.id)
    context['profile'] = profile

    order = Order.objects.filter(restaurant = profile)
    context['orders'] = order

    

    if "update_profile" in request.POST:
        print("file=",request.FILES)
        name = request.POST.get('name')
        contact = request.POST.get('contact_number')
        add = request.POST.get('address')
       
        profile.restaurant_name = name 
        profile.contact_no = contact 
        profile.address = add 

        if "profile_pic" in request.FILES:
            pic = request.FILES['profile_pic']
            profile.res_image = pic

        profile.save()

        context['status'] = f"Profile updated successfully!"

    if "change_pass" in request.POST:
        c_password = request.POST.get('current_password')
        n_password = request.POST.get('new_password')

        check = login_user.check_password(c_password)
        if check==True:
            login_user.set_password(n_password)
            login_user.save()
            login(request, login_user)
            context['status'] = f"Password Updated Successfully!" 
        else:
            context['status'] = f"Current Password Incorrect!"

    return render(request, 'dashboard1.html',context)

def order1(request):
    context={}
    login_user = get_object_or_404(User, id = request.user.id)
    #fetch login user's details
    profile = Restaurant.objects.get(user__id=request.user.id)
    context['profile'] = profile

    order = Order.objects.filter(restaurant = profile)
    context['orders'] = order
    print("h1")

    if request.method == "POST":
        print("h2")
        
        if request.POST.get("submit") == "1":

            status = request.POST.get("order_status")
            orderid = request.POST.get("order_id")
            print("h3")
            Od = Order.objects.get(id = orderid)
            
            Od.status= status
            Od.save()

        if request.POST.get("submit") == "2":

            status = request.POST.get("payment_status")
            orderid = request.POST.get("order_id")
            print("h3")
            Od = Order.objects.get(id = orderid)
            
            Od.payment_status= status
            Od.save()
        

    return render(request, 'order1.html',context)


def user_logout(request):
    order_id = request.session.get('order')

    if order_id:
        print(order_id)
        del request.session['order']

    p = request.session.get('paymnet')

    if p:
        print(p)
        del request.session['payment']
    logout(request)
    return HttpResponseRedirect('/')


#restaurant
def index1(request):
    return render(request,'index1.html')

def about1(request):
    return render(request,'about1.html')

def report1(request):
    context={}
    contxt={}
    id = Restaurant.objects.get(user_id=request.user.id)
    contxt['id'] = id

    # def_user_id = request.user.id
    # print(def_user_id)

    id1 = id.restaurant_id
    
    if request.method== "POST":
        name = request.POST.get("name")
        em = request.POST.get("email")
        sub = request.POST.get("subject")
        pb_wh = request.POST.get("prblem with")
        pb = request.POST.get("message")

        obj = Report(us_id=id1,us_name=name, us_email= em, subject = sub, prob_whom = pb_wh , problem = pb)
        obj.save()
        
        context['message'] =f"Respected {name},Thanks for sharing problem with us will solve it as soon as possible"
    
    return render(request,'report1.html',context)

def menu1(request):
    context={}
    r1 =  Restaurant.objects.get(user_id=request.user.id)
    rest = get_object_or_404(Restaurant, user__id = request.user.id)
    print(request.user.id)
    print(rest)
    print(r1)
    if "add item" in request.POST:
        nme = request.POST.get("item name")
        pri = request.POST.get("item price")
        ind = request.POST.get("ingredients")
        
        obj=Items(Rest=rest,name=nme,price=pri,ingredients=ind)
        
        
        if "item picture" in request.FILES:
            imgw = request.FILES["item picture"]
            obj.image=imgw

        obj.save()
        
        #request.POST.get("item picture")
        context['message']=f"Thanks for your time!"

    mem = Items.objects.filter(Rest = rest).order_by('name')

    context['item_list'] = mem
    
    return render(request,'menu1.html',context)

#Customer
def index2(request):
    return render(request,'index2.html')

def about2(request):
    return render(request,'about2.html')

def report2(request):
    context={}
    contxt={}
    id = Customer.objects.get(user_id=request.user.id)
    contxt['id'] = id

    # def_user_id = request.user.id
    # print(def_user_id)

    id1 = id.customer_id
    
    if request.method== "POST":
        name = request.POST.get("name")
        em = request.POST.get("email")
        sub = request.POST.get("subject")
        pb_wh = request.POST.get("prblem with")
        pb = request.POST.get("message")

        obj = Report(us_id=id1,us_name=name, us_email= em, subject = sub, prob_whom = pb_wh , problem = pb)
        obj.save()
        
        context['message'] =f"Respected {name},Thanks for sharing problem with us will solve it as soon as possible"
    
    return render(request,'report2.html',context)

def dashboard2(request):
    context={}
    login_user = get_object_or_404(User, id = request.user.id)
    #fetch login user's details
    profile = Customer.objects.get(user__id=request.user.id)
    context['profile'] = profile
    print(profile)
    order = Order.objects.filter(customer = profile)
    context['orders'] = order

    # ie = order.paym
    # payment = Payment.objects.filter(id = ie)

    # context['payment'] = 
    #order.paym.amount
    

    if "update_profile" in request.POST:
        print("file=",request.FILES)
        name = request.POST.get('name')
        contact = request.POST.get('contact_number')
        add = request.POST.get('address')
       
        profile.customer_name = name 
        profile.mobile_no = contact 
        profile.address = add 

        if "profile_pic" in request.FILES:
            pic = request.FILES['profile_pic']
            profile.profile_pic = pic

        profile.save()

        context['status'] = 'Profile updated successfully!'
        return render(request, 'dashboard2.html',context)

    if "change_pass" in request.POST:
        c_password = request.POST.get('current_password')
        n_password = request.POST.get('new_password')

        check = login_user.check_password(c_password)
        if check==True:
            login_user.set_password(n_password)
            login_user.save()
            login(request, login_user)
            context['status'] = 'Password Updated Successfully!' 
        else:
            context['status'] = 'Current Password Incorrect!'

    return render(request, 'dashboard2.html',context)

def menu2(request):
    context={}
    
    item1 = Items.objects.filter( Rest_id = 'R001001')
    item2 = Items.objects.filter( Rest_id = 'R002001')
    item3 = Items.objects.filter( Rest_id = 'R003001')
    item4 = Items.objects.filter( Rest_id = 'R004001')
    
    context['item1'] = item1
    context['item2'] = item2
    context['item3'] = item3
    context['item4'] = item4
    #print(context)
    s_key = request.session.session_key
    print(s_key)
    if request.method == 'POST':
        
        item__id = request.POST.get(f"item_id")
        quantity1 = request.POST.get("quanitiy")
        print(item__id)
        print("quantity1 : ")
        print(quantity1)
        global re 
        global b1

        if b1 == 1 :
            item_1 = item__id
            o1 = Items.objects.get(id = item_1)
            print(o1)
            re = o1.Rest.restaurant_id
            print("re" + re)
        
        r1 =re
        print("r1 "+ r1)
        o2 = Items.objects.get(id = item__id)
        print(o2)
        r2 = o2.Rest.restaurant_id
        def incrementb():
                global b1
                b1 = b1 + 1
            
        incrementb()
        print(b1)

        if r2 != r1:
            context['mess'] = f"Select you item of same Restaurant"
            return render(request,'menu2.html',context)

        #print(quantity)
        items = get_object_or_404(Items, pk = item__id)
        s_key = request.session.session_key
        print(s_key)

        if not s_key:
            s_key = request.session.cycle_key()
        
        global a
        a =+ 1 
        print(s_key)
        print("a : ")
        print(a)

        # try:
        #     cart = Cart.objects.get(session_key=s_key)
        # except Cart.DoesNotExist :
        #     cart = Cart(session_key=s_key)
        #     cart.save()

        cart, created = Cart.objects.get_or_create(session_key=s_key)
        
        customer = Customer.objects.get(user__id=request.user.id)
        customer.save()

        cart_item1, created = CartItem.objects.get_or_create(cart1=cart, Cust=customer)
        cart_item1.save()
        cart_item2 = CartItem_Item.objects.filter(cart_item=cart_item1, item=items).first()
        if cart_item2:
            print("cart_item2")
            print(cart_item2)
            cart_item2.quantity += int(quantity1)
            cart_item2.save()
        else:
            cart_item2 = CartItem_Item.objects.create(cart_item=cart_item1, item=items, quantity=int(quantity1))

        #cart_item2, created2 = CartItem_Item.objects.get_or_create(cart_item=cart_item1, item=items, quantity=quantity1)
        
        #if not created2:
            # cart_item3 = CartItem_Item.objects.filter(item_id = item__id)
            # print("cart_item3")
            # print(cart_item3)
            # cart_item3.quantity += 1
            # cart_item3.save()

        print(customer)
        cart_item1.save()
        cart_item2.save()

    print("b1")
    
    print(b1)

    status = request.session.get('status')
    if status:
        del request.session['status']
    context['status'] =  status

    return render(request,'menu2.html',context)




def cart(request):
    context={}

    ss_key = request.session.session_key
    print(ss_key)
    

    try:
        crt = Cart.objects.get(session_key = ss_key)
    except Cart.DoesNotExist:
        context['status'] = 'add some item in cart'
        request.session['status'] = 'add some item in cart'

        return redirect('/menu2/')
    
    print("crt")
    print(crt)

    id3 = crt.id1
    print("id3")
    print(id3)
    
    cart_item1 = CartItem.objects.get(cart1_id=id3)
    print("cart_item1")
    print(cart_item1)

    id4 = cart_item1.id
    print("id4")
    print(id4)
    
    #cart_ii = CartItem_Item.objects.filter(cart_item_id = id4)
    cart_ii = CartItem_Item.objects.filter(cart_item=cart_item1)
    print("cart_ii")
    print(cart_ii)

    #items = cart_ii.item.all()
    context['items'] = cart_ii
    #print(context)

    total_price = 0
    for item in cart_ii:
        total_price += item.get_total_price()

    print("total_price")
    print(total_price)
    context['total_price'] = total_price

    if request.method == 'POST':
        print("hello")

        if request.POST.get('submit') == "2":
            item_id1 = request.POST.get("item_id")
            qua1 = request.POST.get("quantity")

            print("hi")

            id3 = crt.id1
            print("id3")
            print(id3)
            
            cart_item1 = CartItem.objects.get(cart1_id=id3)
            print("cart_item1")
            print(cart_item1)

            cart_ii = CartItem_Item.objects.filter(cart_item=cart_item1)
            print("cart_ii")
            print(cart_ii)

            ob1 = CartItem_Item.objects.filter(item_id = item_id1)
            print("ob1")
            print(ob1)

            q = int(qua1) + 1
            ob1.update(quantity = q)
            
            #ob1.save()
            id3 = crt.id1
            print("id3")
            print(id3)
            
            cart_item1 = CartItem.objects.get(cart1_id=id3)
            print("cart_item1")
            print(cart_item1)

            id4 = cart_item1.id
            print("id4")
            print(id4)
            
            #cart_ii = CartItem_Item.objects.filter(cart_item_id = id4)
            cart_ii = CartItem_Item.objects.filter(cart_item=cart_item1)
            print("cart_ii")
            print(cart_ii)

            #items = cart_ii.item.all()
            context['items'] = cart_ii

            total_price = 0
            for item in cart_ii:
                total_price += item.get_total_price()

            print("total_price")
            print(total_price)
            context['total_price'] = total_price
            
            return render(request,'cart.html',context)
        
        if request.POST.get('submit') == "1":
            item_id1 = request.POST.get("item_id")
            qua1 = request.POST.get("quantity")

            print("hi2")

            id3 = crt.id1
            print("id3")
            print(id3)
            
            cart_item1 = CartItem.objects.get(cart1_id=id3)
            print("cart_item1")
            print(cart_item1)

            cart_ii = CartItem_Item.objects.filter(cart_item=cart_item1)
            print("cart_ii")
            print(cart_ii)

            ob1 = CartItem_Item.objects.filter(item_id = item_id1)
            print(ob1)
            
            q = int(qua1) - 1

            if q == 0:
                q =1

            ob1.update(quantity = q)
            
            #ob1.save()
            id3 = crt.id1
            print("id3")
            print(id3)
            
            cart_item1 = CartItem.objects.get(cart1_id=id3)
            print("cart_item1")
            print(cart_item1)

            id4 = cart_item1.id
            print("id4")
            print(id4)
            
            #cart_ii = CartItem_Item.objects.filter(cart_item_id = id4)
            cart_ii = CartItem_Item.objects.filter(cart_item=cart_item1)
            print("cart_ii")
            print(cart_ii)

            #items = cart_ii.item.all()
            context['items'] = cart_ii

            total_price = 0
            for item in cart_ii:
                total_price += item.get_total_price()

            print("total_price")
            print(total_price)
            context['total_price'] = total_price
            
            return render(request,'cart.html',context)
        
        if request.POST.get('submit') == "4":
            
            setb1()

            id3 = crt.id1
            print("id3")
            print(id3)
            
            cart_item1 = CartItem.objects.get(cart1_id=id3)
            print("cart_item1")
            print(cart_item1)

            id4 = cart_item1.id
            print("id4")
            print(id4)
            
            #cart_ii = CartItem_Item.objects.filter(cart_item_id = id4)
            cart_ii = CartItem_Item.objects.filter(cart_item=cart_item1).delete()
            #cart_ii = CartItem_Item.objects.delete(cart_item=cart_item1)
            print("cart_ii")
            print(cart_ii)

            id3 = crt.id1
            print("id3")
            print(id3)
            
            cart_item1 = CartItem.objects.get(cart1_id=id3)
            print("cart_item1")
            print(cart_item1)

            id4 = cart_item1.id
            print("id4")
            print(id4)
            
            #cart_ii = CartItem_Item.objects.filter(cart_item_id = id4)
            cart_ii = CartItem_Item.objects.filter(cart_item=cart_item1)
            print("cart_ii")
            print(cart_ii)

            #items = cart_ii.item.all()
            context['items'] = cart_ii

            total_price = 0
            context['total_price'] = total_price

            return render(request,'cart.html',context)
        
        if type(request.POST) is not dict:
            request.POST = request.POST.dict()

        if request.POST.get('submit') == "3":

            item_id5 = request.POST.get("item_id")
            print("item_id5")
            print(item_id5)
            setb1()
            c = Customer.objects.get(user__id=request.user.id)
            
            r = Items.objects.filter(id = item_id5)
            print("r")
            print(r)

            for i in r:
                r2 = i.get_rest()

            print("r2")
            print(r2)

            ord1 = Order.objects.filter(customer=c, restaurant=r2, cart_item=cart_item1).first()
            if ord1 is None:
                ord1 = Order(customer=c, restaurant=r2, cart_item=cart_item1)
            ord1.order_time = timezone.now()
            ord1.save()

            request.session['order'] = ord1.id
            # context['order'] = ord1
            # ct = ord1.cart_item
            # ct1 = ct.cart1.id1

            # ct2 = CartItem_Item.objects.filter(cart_item_id = ct1)
            # print("ct2")
            # print(ct2)
            # context['c'] = ct2

            return redirect('/final_order/')

    return render(request,'cart.html',context)

def setb1():
    global b1
    b1 =1

def final_order(request):
    context = {}
    order_id = request.session.get('order')
    
    if request.method == 'POST':
        print("hello")

        if request.POST.get('submit') == "1":

            print("hi")
            nm = request.POST.get("name")
            ph = request.POST.get("phone")
            ad = request.POST.get("address")

            order = Order.objects.get(id=order_id)

            order.name = nm
            order.mo_no = ph
            order.add = ad
            print(nm)
            print(ph)
            print(ad)

            order.save()

        if request.POST.get('submit') == "2":

            print("h")
            am = request.POST.get("amount")
            print(am)
            
            order = Order.objects.get(id=order_id)
            pay = Payment.objects.get_or_create(customer = order.customer , amount =am)
            print("pay")
            print(pay)
            order.paym = pay[0]

            order.save()
            p = pay[0].id
            
            request.session['payment'] = p
            return redirect('/payment')

    if order_id:
        # Retrieve the Order object from the database
        order = Order.objects.get(id=order_id)

        # Remove the order from the session
        #del request.session['order']
        ct = order.cart_item
        ct1 = ct.id

        ct2 = CartItem_Item.objects.filter(cart_item_id = ct1).all()
        print("ct2")
        print(ct2)

        total_price = 0
        for item in ct2:
            total_price += item.get_total_price()

        

        print("total_price")
        print(total_price)
        context['total_price'] = total_price

        context['c'] = ct2

        cu = order.customer.customer_name
        cadd = order.customer.address
        cm = order.customer.mobile_no

        print(order)
        context['order'] = order
            
    return render(request,'final_order.html',context)

import random

def generate_otp1():
    """Generate a random 4-digit OTP"""
    digits = [str(random.randint(0, 9)) for _ in range(4)]
    print(digits)
    return ''.join(digits)


def genrate_otp(request):
    context ={}
    
    if request.method == "POST":
        print("hi")
        st = generate_otp1()
        print(st)
        request.session['otp'] = st
        context['otp'] = st
        context['otp_generated'] = True
        return render(request,'genrate_otp.html',context)
    
    
    return render(request,'genrate_otp.html',context)

def map_view(request):

    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request,'map.html',context)

def payment(request):

    context = {}
    order_id = request.session.get('order')
    order = Order.objects.get(id=order_id)
    pay_id = request.session.get('payment')
    payment = Payment.objects.get(id=pay_id)

    otp = request.session.get('otp')
    
    context['order'] = order
    context['payment'] = payment

    if request.method == "POST":
        
        payment_method = request.POST.get('payment_method')
        otp1 = request.POST.get('otp')
        
        if payment_method == 'online' and not otp:
            context['error'] = 'Please enter OTP.'
            return render(request, 'payment.html', context)
        
        if otp1 == otp:
            order.payment_status=2
            order.status=2
            order.save()
            return redirect('/dashboard2')
        elif payment_method == 'cod':
            order.payment_status=1
            order.status=2
            order.save()
            return redirect('/dashboard2')
        else:
            context['error'] = 'payment failed'
            return render(request,'dashboard2.html',context)

            
        return redirect('/dashboard2')
        

    return render(request,'payment.html',context)