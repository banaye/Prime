from django.urls import path
from . import views

urlpatterns = [
    # ==================== PHONE URLS ====================
    path('phones/', views.PhoneListView.as_view(), name='phone_list'),
    path('phones/<int:pk>/', views.PhoneDetailView.as_view(), name='phone_detail'),
    path('phones/create/', views.PhoneCreateView.as_view(), name='phone_create'),
    path('phones/<int:pk>/edit/', views.PhoneUpdateView.as_view(), name='phone_update'),
    path('phones/<int:pk>/delete/', views.PhoneDeleteView.as_view(), name='phone_delete'),
    
    # ==================== ACCESSORIES URLS ====================
    path('accessories/', views.AccessoriesListView.as_view(), name='accessories_list'),
    path('accessories/<int:pk>/', views.AccessoriesDetailView.as_view(), name='accessory_detail'),
    path('accessories/create/', views.AccessoriesCreateView.as_view(), name='accessory_create'),
    path('accessories/<int:pk>/edit/', views.AccessoriesUpdateView.as_view(), name='accessory_update'),
    path('accessories/<int:pk>/delete/', views.AccessoriesDeleteView.as_view(), name='accessory_delete'),
    
    # ==================== SHOPPING CART URLS ====================
    path('cart/add/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart_view'),
    path('cart/remove/<str:cart_item_key>/', views.remove_from_cart, name='remove_from_cart'),
    
    # ==================== ORDER URLS ====================
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    
    # ==================== REVIEW URLS ====================
    path('reviews/add/<str:item_type>/<int:item_id>/', views.add_review, name='add_review'),
    
    # ==================== CUSTOMER PROFILE URLS ====================
    path('profile/', views.customer_profile, name='customer_profile'),
]
