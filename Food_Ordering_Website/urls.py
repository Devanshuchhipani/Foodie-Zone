"""Food_Ordering_Website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Foodie_Zone import views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('about/',views.about,name="about"),
    path('partner/',views.partner,name="partner"),
    path('contact/',views.contact_us,name="contact"),
    path('register/',views.register,name="register"),
    path('check_user_exists/',views.check_user_exists,name="check_user_exist"),
    path('login/', views.signin, name='login'),
    path('dashboard1/', views.dashboard1, name='dashboard1'),
    path('logout/', views.user_logout, name='logout'),
    path('index1/',views.index1,name="index1"),
    path('about1/',views.about1,name="about1"),
    path('report1/',views.report1,name="report1"),
    path('menu1/',views.menu1,name="menu1"),
    path('menu/',views.menu,name="menu"),
    path('index2/',views.index2,name="index2"),
    path('about2/',views.about2,name="about2"),
    path('dashboard2/', views.dashboard2, name='dashboard2'),
    path('report2/',views.report2,name="report2"),
    path('menu2/',views.menu2,name="menu2"),
    path('cart/',views.cart,name="cart"),
    path('final_order/',views.final_order,name="final_order"),
    path('genrate_otp/',views.genrate_otp,name="genrate_otp"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
