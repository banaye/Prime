from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from decimal import Decimal
from .models import Phone, Accessories, Category, Order, OrderItem, CustomerProfile, Review


# ==================== PHONE VIEWS ====================

class PhoneListView(ListView):
    model = Phone
    template_name = 'prime_accessories/phone_list.html'
    context_object_name = 'phones'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Phone.objects.all()
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(brand__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__id=category)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by condition
        condition = self.request.GET.get('condition')
        if condition:
            queryset = queryset.filter(condition=condition)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        return context


class PhoneDetailView(DetailView):
    model = Phone
    template_name = 'prime_accessories/phone_detail.html'
    context_object_name = 'phone'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['compatible_accessories'] = self.object.accessories.all()
        return context


@method_decorator(login_required, name='dispatch')
class PhoneCreateView(CreateView):
    model = Phone
    template_name = 'prime_accessories/phone_form.html'
    fields = ['name', 'brand', 'model', 'description', 'price', 'stock', 'processor', 
              'ram', 'storage', 'display_size', 'camera_mp', 'battery_mah', 'os', 
              'condition', 'color', 'image_url', 'category']
    success_url = reverse_lazy('phone_list')


@method_decorator(login_required, name='dispatch')
class PhoneUpdateView(UpdateView):
    model = Phone
    template_name = 'prime_accessories/phone_form.html'
    fields = ['name', 'brand', 'model', 'description', 'price', 'stock', 'processor', 
              'ram', 'storage', 'display_size', 'camera_mp', 'battery_mah', 'os', 
              'condition', 'color', 'image_url', 'category']
    success_url = reverse_lazy('phone_list')


@method_decorator(login_required, name='dispatch')
class PhoneDeleteView(DeleteView):
    model = Phone
    template_name = 'prime_accessories/phone_confirm_delete.html'
    success_url = reverse_lazy('phone_list')


# ==================== ACCESSORIES VIEWS ====================

class AccessoriesListView(ListView):
    model = Accessories
    template_name = 'prime_accessories/accessories_list.html'
    context_object_name = 'accessories'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Accessories.objects.all()
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(accessory_type__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__id=category)
        
        # Filter by accessory type
        accessory_type = self.request.GET.get('type')
        if accessory_type:
            queryset = queryset.filter(accessory_type=accessory_type)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        return context


class AccessoriesDetailView(DetailView):
    model = Accessories
    template_name = 'prime_accessories/accessory_detail.html'
    context_object_name = 'accessory'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['compatible_phones'] = self.object.compatible_phones.all()
        return context


@method_decorator(login_required, name='dispatch')
class AccessoriesCreateView(CreateView):
    model = Accessories
    template_name = 'prime_accessories/accessory_form.html'
    fields = ['name', 'brand', 'description', 'price', 'stock', 'accessory_type', 
              'color', 'material', 'compatible_phones', 'image_url', 'category']
    success_url = reverse_lazy('accessories_list')


@method_decorator(login_required, name='dispatch')
class AccessoriesUpdateView(UpdateView):
    model = Accessories
    template_name = 'prime_accessories/accessory_form.html'
    fields = ['name', 'brand', 'description', 'price', 'stock', 'accessory_type', 
              'color', 'material', 'compatible_phones', 'image_url', 'category']
    success_url = reverse_lazy('accessories_list')


@method_decorator(login_required, name='dispatch')
class AccessoriesDeleteView(DeleteView):
    model = Accessories
    template_name = 'prime_accessories/accessory_confirm_delete.html'
    success_url = reverse_lazy('accessories_list')


# ==================== SHOPPING CART & ORDER VIEWS ====================

@login_required
def add_to_cart(request, item_type, item_id):
    """Add phone or accessory to cart (session-based)"""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    cart_item_key = f"{item_type}_{item_id}"
    
    if cart_item_key in request.session['cart']:
        request.session['cart'][cart_item_key]['quantity'] += 1
    else:
        if item_type == 'phone':
            item = get_object_or_404(Phone, id=item_id)
        else:
            item = get_object_or_404(Accessories, id=item_id)
        
        request.session['cart'][cart_item_key] = {
            'item_type': item_type,
            'item_id': item_id,
            'name': item.name,
            'price': str(item.price),
            'quantity': 1
        }
    
    request.session.modified = True
    return redirect('cart_view')


@login_required
def view_cart(request):
    """Display shopping cart"""
    cart = request.session.get('cart', {})
    cart_items = []
    total_amount = Decimal('0.00')
    
    for cart_item_key, item in cart.items():
        item['subtotal'] = Decimal(item['price']) * item['quantity']
        total_amount += item['subtotal']
        cart_items.append(item)
    
    return render(request, 'prime_accessories/cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })


@login_required
def remove_from_cart(request, cart_item_key):
    """Remove item from cart"""
    if 'cart' in request.session and cart_item_key in request.session['cart']:
        del request.session['cart'][cart_item_key]
        request.session.modified = True
    
    return redirect('cart_view')


@login_required
def checkout(request):
    """Process order"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        
        if not cart:
            return redirect('cart_view')
        
        # Create order
        total_amount = Decimal('0.00')
        for item in cart.values():
            total_amount += Decimal(item['price']) * item['quantity']
        
        discount = Decimal(request.POST.get('discount', 0))
        final_amount = total_amount - discount
        
        order = Order.objects.create(
            customer=request.user,
            order_number=f"ORD-{request.user.id}-{Order.objects.count() + 1}",
            total_amount=total_amount,
            discount=discount,
            final_amount=final_amount,
            shipping_address=request.POST.get('shipping_address'),
            notes=request.POST.get('notes', '')
        )
        
        # Create order items
        for cart_item_key, item in cart.items():
            OrderItem.objects.create(
                order=order,
                item_type=item['item_type'],
                phone_id=item['item_id'] if item['item_type'] == 'phone' else None,
                accessory_id=item['item_id'] if item['item_type'] == 'accessory' else None,
                quantity=item['quantity'],
                unit_price=Decimal(item['price']),
                total_price=Decimal(item['price']) * item['quantity']
            )
        
        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True
        
        return redirect('order_detail', pk=order.id)
    
    return render(request, 'prime_accessories/checkout.html')


class OrderListView(ListView):
    model = Order
    template_name = 'prime_accessories/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'prime_accessories/order_detail.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


# ==================== REVIEW VIEWS ====================

@login_required
def add_review(request, item_type, item_id):
    """Add review for phone or accessory"""
    if request.method == 'POST':
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        review_text = request.POST.get('review_text')
        
        if item_type == 'phone':
            phone = get_object_or_404(Phone, id=item_id)
            Review.objects.create(
                phone=phone,
                customer=request.user,
                rating=rating,
                title=title,
                review_text=review_text
            )
            return redirect('phone_detail', pk=item_id)
        else:
            accessory = get_object_or_404(Accessories, id=item_id)
            Review.objects.create(
                accessory=accessory,
                customer=request.user,
                rating=rating,
                title=title,
                review_text=review_text
            )
            return redirect('accessory_detail', pk=item_id)
    
    return render(request, 'prime_accessories/add_review.html', {
        'item_type': item_type,
        'item_id': item_id
    })


# ==================== CUSTOMER PROFILE VIEWS ====================

@login_required
def customer_profile(request):
    """Display and edit customer profile"""
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.phone_number = request.POST.get('phone_number')
        profile.address = request.POST.get('address')
        profile.city = request.POST.get('city')
        profile.state = request.POST.get('state')
        profile.zip_code = request.POST.get('zip_code')
        profile.country = request.POST.get('country')
        profile.save()
        
        return redirect('customer_profile')
    
    return render(request, 'prime_accessories/customer_profile.html', {'profile': profile})