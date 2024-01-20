from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.



# CATEGORY_CHOICES={
#     ('CR','Curd'),
#     ('ML','Milk'),
#     ('LS','Lassi'),
#     ('MS','Milk Shake'),
#     ('PN','Paneer'),
#     ('GH','Ghee'),
#     ('CZ','Cheese'),
#     ('IC','Ice-Cream'),
    
# }

class ProductCategory(models.Model):
    #id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name
        

# class Product(models.Model):
#     title = models.CharField(max_length=100)
#     selling_price= models.FloatField()
#     discounted_price = models.FloatField()
#     description = models.TextField()
#     composition = models.TextField(default ='')
#     prodapp = models.TextField(default='')
#     #category = models.CharField(choices = CATEGORY_CHOICES, max_length=2)
#     category  =models.ForeignKey(ProductCategory,on_delete=models.CASCADE)    
#     manufactor_date=models.CharField(max_length=100,default='')
#     useby_date=models.CharField(max_length=100,default='')
#     product_image= models.ImageField(upload_to='product')
#     #slug = models.SlugField(unique=True,default='')


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField(blank=True, null=True)
    discounted_price = models.FloatField(blank=True, null=True)
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    manufactor_date = models.DateTimeField(blank=True, null=True)  # Change to DateTimeField
    useby_date = models.DateTimeField(blank=True, null=True)
    product_image = models.ImageField(upload_to='product')
    stock_quantity = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Set manufactor_date to login date
        if not self.manufactor_date:
            self.manufactor_date = timezone.now()

        # Calculate useby_date as 48 hours from manufactor_date
        if not self.useby_date:
            self.useby_date = self.manufactor_date + timezone.timedelta(hours=48)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class ProductVariation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,default='')
    quantity = models.CharField(max_length=50)  # e.g., '1 litre', '500 ml', '250 ml'
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    def __str__(self):
        return self.quantity

STATE_CHOICES = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Delhi', 'Delhi'),
    ('Puducherry', 'Puducherry'),
)   
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    pincode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    
    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE) 
    quantity = models.PositiveBigIntegerField(default=1)
    
   
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price 
    

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null =True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.amount)
    
    

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
    
)
class OrderPlaced(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer =models.ForeignKey(Customer,on_delete=models.CASCADE)
    product =models.ForeignKey(Product,on_delete=models.CASCADE,default=1,null=True)
    quantity =models.PositiveIntegerField(default=1)
    ordereded_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
   
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    

