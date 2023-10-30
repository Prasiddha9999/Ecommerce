from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    cat_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='media/images', default=None)
    desc = models.TextField(max_length=255)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # Add the 'status' field with choices
    STATUS_CHOICES = (
        ('in_cart', 'In Cart'),
        ('ordered', 'Ordered'),
        ('shipped', 'Shipped'),
        # Add more status choices as needed
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_cart')

    def __str__(self):
        return f"{self.quantity} x {self.item} in {self.user}'s cart"
    

class Order(models.Model):
    # Your other fields here
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Add the 'action' field with extended choices
    ACTION_CHOICES = (
        ('pending', 'Pending'),
        ('received_by_owner', 'Received by Owner'),
        ('confirm', 'Confirm'),
        ('reject', 'Reject'),
        ('on_the_way', 'On the Way'),
        # Add more status choices as needed
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, default='pending')
    
    def __str__(self):
        return f"Order #{self.pk} by {self.user} on {self.created_at}"



