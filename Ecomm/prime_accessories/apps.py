from django.apps import AppConfig
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import admin
from .models import Phone, Accessories, Category, Order, OrderItem, CustomerProfile, Review
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['-created_at']
    
@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'stock', 'rating', 'condition', 'created_at']
    list_filter = ['condition', 'rating', 'created_at', 'category']
    search_fields = ['name', 'brand', 'model']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'brand', 'model', 'description', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock')
        }),
        ('Specifications', {
            'fields': ('processor', 'ram', 'storage', 'display_size', 'camera_mp', 'battery_mah', 'os')
        }),
        ('Additional Info', {
            'fields': ('condition', 'color', 'image_url', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
@admin.register(Accessories)
class AccessoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'accessory_type', 'price', 'stock', 'rating', 'created_at']
    list_filter = ['accessory_type', 'rating', 'created_at', 'category']
    search_fields = ['name', 'brand', 'accessory_type']
    filter_horizontal = ['compatible_phones']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'brand', 'accessory_type', 'description', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock')
        }),
        ('Details', {
            'fields': ('color', 'material', 'compatible_phones', 'image_url', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer__user__username']
    readonly_fields = ['created_at', 'updated_at']
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'content_object', 'quantity', 'price']
    search_fields = ['order__customer__user__username']
    
@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):    
    list_display = ['user', 'phone_number', 'city', 'country', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['user__username', 'phone_number', 'city']
    readonly_fields = ['created_at', 'updated_at']
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'content_object', 'rating', 'created_at']
    search_fields = ['customer__user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    

class PrimeAccessoriesConfig(AppConfig):
    name = 'prime_accessories'
    verbose_name = "Prime Accessories Store"
    
    def ready(self):
        # Import signal handlers
        import prime_accessories.signals
        
    
