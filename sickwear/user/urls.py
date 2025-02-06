"""sickwear URL Configuration

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
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('staff-member-page', views.staff_member_page, name='staffMmberPage'),

    path('staff/dashboard/', views.StaffDashboardView.as_view(), name='staff-dashboard'),
    
    # Users
    path('staff/users/', views.UserListView.as_view(), name='staff-users'),
    
    # Products
    path('staff/products/', views.ProductListView.as_view(), name='staff-products'),
    path('staff/products/add/', views.ProductCreateView.as_view(), name='staff-product-add'),
    path('staff/products/<int:pk>/', views.ProductUpdateView.as_view(), name='staff-product-edit'),
    
    # Orders
    path('staff/orders/', views.OrderListView.as_view(), name='staff-orders'),
    path('staff/orders/<int:pk>/', views.OrderUpdateView.as_view(), name='staff-order-edit'),
    
    # Add similar paths for other models
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
