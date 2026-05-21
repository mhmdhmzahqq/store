from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # نظام الحماية
    path('register/', views.register_account, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # العملاء
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/new/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),

    # المنتجات
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/new/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # الطلبات
    path('', views.OrderListView.as_view(), name='order_list'),
    path('orders/new/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('api/customers/', views.CustomerListCreateAPI.as_view(), name='api_customers'),
    path('api/products/', views.ProductListCreateAPI.as_view(), name='api_products'),
    path('api/orders/', views.OrderListCreateAPI.as_view(), name='api_orders'),

    # ***********************************************************fbv********************************************
    # # الحماية
    # path('register/', views.register_account, name='register'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),

    # # العملاء
    # path('customers/', views.customer_list, name='customer_list'),
    # path('customers/new/', views.customer_create, name='customer_create'),
    # path('customers/<int:pk>/edit/', views.customer_update, name='customer_update'),
    # path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),

    # # المنتجات
    # path('products/', views.product_list, name='product_list'),
    # path('products/new/', views.product_create, name='product_create'),
    # path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    # path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # # الطلبات
    # path('orders/', views.order_list, name='order_list'),
    # path('orders/new/', views.order_create, name='order_create'),
    # path('orders/<int:pk>/edit/', views.order_update, name='order_update'),
    # path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
]