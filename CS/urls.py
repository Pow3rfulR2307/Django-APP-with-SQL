"""CS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from app1 import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.index, name='index'), 
    path('register/', views.register_user, name='register'),
    path('register-freelas/', views.register_freelancer, name='freelas_register'),
    path('login/', views.login_user, name='login'),
    path('register_user/', views.register_user_view, name='register_user'),
    path('login_user/', views.login_user_view, name='login_user'),
    path('about/', views.about_view, name='about'),
    path('features/', views.features_view, name='features'),
    path('search-freelancers/', views.search_freelancers_view, name='search_freelancers'),
    path('filter_freelas/', views.filtered_freelancers_view, name='filter_freelas'),
    path('profile/', views.profile_view, name='profile'),
    path('register-freelancer/', views.register_freelancer_view, name='register_freelancer'),
    path('client-dashboard/', views.client_dashboard_view, name='client_dashboard'),
    path('freelancer-dashboard/', views.freelancer_dashboard_view, name='freelancer_dashboard'),
    path('delete/', views.delete_account, name = 'delete_account'),
    path('create-invoice/', views.create_invoice_view, name = 'create_invoice'),
    path('submit_invoice/', views.submit_invoice, name = 'submit_invoice'),
    path('profile-freelancer/', views.profile_freelancer_view, name = 'profile_freelancer'),
    path('delete_freelas/', views.delete_freelancer, name = 'delete_freelancer_account'),
    path('logout/', views.logout_freelas_user, name = 'logout'),
    path('pay_invoice/', views.pay_invoice, name = 'pay_invoice'),
    path('about-freelas/<str:freelancer_email>/', views.about_freelancer, name='about_freelancer'),
    path('conclude_job/', views.finish_invoice, name='finish_invoice')
]