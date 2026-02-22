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


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'country', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['user__username', 'phone_number', 'city']
    readonly_fields = ['created_at', 'updated_at']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'total_amount', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'customer__username']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'customer')
        }),
        ('Financial', {
            'fields': ('total_amount', 'discount', 'final_amount')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Shipping', {
            'fields': ('shipping_address', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'rating', 'is_verified_purchase', 'created_at']
    list_filter = ['rating', 'is_verified_purchase', 'created_at']
    search_fields = ['title', 'customer__username', 'review_text']
    readonly_fields = ['created_at', 'updated_at', 'helpful_count']
    fieldsets = (
        ('Review Info', {
            'fields': ('phone', 'accessory', 'customer', 'rating', 'title', 'review_text')
        }),
        ('Meta', {
            'fields': ('is_verified_purchase', 'helpful_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
