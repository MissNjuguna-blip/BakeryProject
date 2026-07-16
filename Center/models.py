from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User (AbstractUser):
    ROLES = [
        ('ADMIN', 'Admin'),
        ('CUSTOMER', 'Customer'),
        ('DELIVERER', 'Deliverer')
    ]

    role = models.CharField(max_length=50)

    def __str__(self):
        return f"Welcome,{self.username}"
    

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def touch(self):
        self.save(update_fields=["updated_at"])

    class Meta:
        abstract = True

class Admin(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="admin_profile")
    phone = models.CharField(max_length=20,unique=True)
    profile_image= models.ImageField(upload_to='Admin/profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} created."

class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="customer_profile", null=True)
    phone = models.CharField(max_length=20,unique=True)
    address = models.TextField()
    profile_image= models.ImageField(upload_to='Customer/profiles/', null=True, blank=True)


    def __str__(self):
        return self.user.username

class Deliverer(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="deliverer_profile", null=True,blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20,unique=True)
    # assigned_order=models.ForeignKey(Customer, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    profile_image= models.ImageField(upload_to='Deliverer/profiles/', null=True, blank=True)

    def __str__(self):
        return self.name
    

class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name,self.image
    

class Order(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("received", "Received"),
        ("preparing", "Preparing"),
        ("ready", "Ready"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    deliverer = models.ForeignKey(Deliverer,on_delete=models.SET_NULL,null=True,blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    delivery_address = models.TextField()
    delivered_at = models.DateTimeField(null=True,blank=True)

    def update_total(self):
        self.total_amount = sum(
            item.quantity * item.unit_price
            for item in self.items.all()
        )
        self.save(update_fields=["total_amount"])


    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.unit_price
    

class Payment(BaseModel):
    PAYMENT_METHODS = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("mpesa", "M-Pesa"),
    ]

    STATUS = [
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("paid", "Paid"),
    ("failed", "Failed"),
    ("cancelled", "Cancelled"),
    ("refunded", "Refunded"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True,unique=True)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    paid_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.order} - {self.status}"

class Gallery(BaseModel):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=1000)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


