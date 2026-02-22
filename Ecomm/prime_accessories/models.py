from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


# Phone Model
class Phone(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('refurbished', 'Refurbished'),
        ('used', 'Used'),
    ]
    
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Technical specifications
    processor = models.CharField(max_length=100, blank=True)
    ram = models.CharField(max_length=50, blank=True)  # e.g., "8GB", "12GB"
    storage = models.CharField(max_length=50, blank=True)  # e.g., "128GB", "256GB"
    display_size = models.CharField(max_length=50, blank=True)  # e.g., "6.1 inches"
    camera_mp = models.CharField(max_length=100, blank=True)  # e.g., "48MP"
    battery_mah = models.IntegerField(blank=True, null=True)
    os = models.CharField(max_length=100, blank=True)  # e.g., "Android 14", "iOS 17"
    
    # Additional info
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    color = models.CharField(max_length=50, blank=True)
    image_url = models.URLField(blank=True)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='phones')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.brand} {self.name}"
    
    class Meta:
        verbose_name_plural = "Phones"
        ordering = ['-created_at']


# Accessories Model
class Accessories(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Accessory specific
    accessory_type = models.CharField(max_length=100)  # e.g., "Screen Protector", "Case", "Charger"
    color = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=100, blank=True)
    compatible_phones = models.ManyToManyField(Phone, related_name='accessories', blank=True)
    
    image_url = models.URLField(blank=True)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='accessories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Accessories"
        ordering = ['-created_at']


# Customer Profile Model
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    shipping_address = models.TextField()
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.order_number}"
    
    class Meta:
        ordering = ['-created_at']


# Order Items Model
class OrderItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('accessory', 'Accessory'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    
    phone = models.ForeignKey(Phone, on_delete=models.SET_NULL, null=True, blank=True)
    accessory = models.ForeignKey(Accessories, on_delete=models.SET_NULL, null=True, blank=True)
    
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        item = self.phone or self.accessory
        return f"{item} - Order {self.order.order_number}"


# Review/Rating Model
class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    accessory = models.ForeignKey(Accessories, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    review_text = models.TextField()
    
    is_verified_purchase = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        item = self.phone or self.accessory
        return f"Review by {self.customer.username} on {item}"
    
    class Meta:
        ordering = ['-created_at']
    
    
