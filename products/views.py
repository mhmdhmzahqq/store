from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin , PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Customer, Product, Order
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, permission_required
from .models import Customer, Product, Order
from .forms import CustomerForm, ProductForm, OrderForm
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer
# ==========================================
# --- نظام الحسابات والمصادقة (FBV) ---
# ==========================================

def register_account(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    # نستخدم قالب auth_form.html ونمرر له المتغير title
    return render(request, 'products/auth_form.html', {'form': form, 'title': 'إنشاء حساب جديد'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('order_list') # التوجيه لصفحة الطلبات بعد تسجيل الدخول
    else:
        form = AuthenticationForm()
    return render(request, 'products/auth_form.html', {'form': form, 'title': 'تسجيل الدخول'})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

# --- العملاء (Customers) ---
class CustomerListView(ListView):
    model = Customer
    template_name = 'products/customer_list.html'
    context_object_name = 'customers'

class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Customer
    fields = '__all__'
    template_name = 'products/form.html'
    success_url = reverse_lazy('customer_list')
    permission_required = 'products.add_customer'
    def get_context_data(self, **kwargs):
        return super().get_context_data(title="إضافة عميل جديد", **kwargs)

class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Customer
    fields = '__all__'
    template_name = 'products/form.html'
    success_url = reverse_lazy('customer_list')
    permission_required = 'products.change_customer'
    def get_context_data(self, **kwargs):
        return super().get_context_data(title="تعديل بيانات العميل", **kwargs)

class CustomerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Customer
    template_name = 'products/confirm_delete.html'
    success_url = reverse_lazy('customer_list')
    permission_required = 'products.delete_customer'

# --- المنتجات (Products) ---
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    fields = '__all__'
    template_name = 'products/form.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'products.add_product'
    def get_context_data(self, **kwargs):
        return super().get_context_data(title="إضافة منتج جديد", **kwargs)

class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'products/form.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'products.change_product'
    def get_context_data(self, **kwargs):
        return super().get_context_data(title="تعديل بيانات المنتج", **kwargs)

class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/confirm_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'products.delete_product'

# --- الطلبات (Orders) ---
class OrderListView(ListView):
    model = Order
    template_name = 'products/order_list.html'
    context_object_name = 'orders'

class OrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Order
    fields = ['customer', 'product', 'quantity'] 
    template_name = 'products/form.html'
    success_url = reverse_lazy('order_list')
    permission_required = 'products.add_order'
    def get_context_data(self, **kwargs):
        return super().get_context_data(title="إنشاء طلب جديد", **kwargs)

class OrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Order
    fields = ['customer', 'product', 'quantity']
    template_name = 'products/form.html'
    success_url = reverse_lazy('order_list')
    permission_required = 'products.change_order'
    def get_context_data(self, **kwargs):
        return super().get_context_data(title="تعديل الطلب", **kwargs)

class OrderDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Order
    template_name = 'products/confirm_delete.html'
    success_url = reverse_lazy('order_list')
    permission_required = 'products.delete_order'


# ==========================================
# --- واجهة برمجة التطبيقات (API Layer) ---
# ==========================================

class CustomerListCreateAPI(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class ProductListCreateAPI(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class OrderListCreateAPI(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


#********************************************************************************fbv**************************************************************
# ==========================================
# --- إدارة العملاء (Customers FBV) ---
# ==========================================

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'products/customer_list.html', {'customers': customers})

@login_required
@permission_required('products.add_customer')
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'products/form.html', {'form': form, 'title': 'إضافة عميل جديد'})

@login_required
@permission_required('products.change_customer')
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'products/form.html', {'form': form, 'title': 'تعديل بيانات العميل'})

@login_required
@permission_required('products.delete_customer')
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    # مررنا المتغير باسم object ليتوافق مع القالب المشترك
    return render(request, 'products/confirm_delete.html', {'object': customer})


# ==========================================
# --- إدارة المنتجات (Products FBV) ---
# ==========================================

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

@login_required
@permission_required('products.add_product')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/form.html', {'form': form, 'title': 'إضافة منتج جديد'})

@login_required
@permission_required('products.change_product')
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/form.html', {'form': form, 'title': 'تعديل بيانات المنتج'})

@login_required
@permission_required('products.delete_product')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/confirm_delete.html', {'object': product})
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/form.html', {'form': form, 'title': 'تعديل بيانات المنتج'})

@login_required
@permission_required('products.delete_product')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/confirm_delete.html', {'object': product})


# ==========================================
# --- إدارة الطلبات (Orders FBV) ---
# ==========================================

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'products/order_list.html', {'orders': orders})

@login_required
@permission_required('products.add_order')
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'products/form.html', {'form': form, 'title': 'إنشاء طلب جديد'})

@login_required
@permission_required('products.change_order')
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'products/form.html', {'form': form, 'title': 'تعديل الطلب'})

@login_required
@permission_required('products.delete_order')
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'products/confirm_delete.html', {'object': order})