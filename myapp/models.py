from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	address=models.TextField()
	password=models.CharField(max_length=100)
	profile_pic=models.ImageField(upload_to="profile_pic/")
	usertype=models.CharField(max_length=100,default="user")


	def __str__(self):
		return self.fname+" "+self.usertype

class Product(models.Model):

	CHOICE=(
		('Computer','Computer'),
		('Laptop','Laptop'),
		('Accessories','Accessories'),

		)
	seller=models.ForeignKey(User,on_delete=models.CASCADE)
	product_category=models.CharField(max_length=100,choices=CHOICE)
	product_name=models.CharField(max_length=100)
	product_price=models.PositiveIntegerField()
	product_desc=models.TextField()
	product_image=models.ImageField(upload_to="product_image/")
	discount=models.PositiveIntegerField()

	def __str__(self):
		return self.product_name+" - "+self.seller.fname

class Wishlist(models.Model):
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.fname+" - "+self.product.product_name

class Cart(models.Model):
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	product_qty=models.PositiveIntegerField(default=1)
	product_price=models.PositiveIntegerField()
	total_price=models.PositiveIntegerField()
	payment_status=models.BooleanField(default=False)

	def __str__(self):
		return self.user.fname+" - "+self.product.product_name

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

class Subscribe(models.Model):
	email=models.EmailField()

	def _str_(self):
		return self.email

class Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	remarks=models.TextField(max_length=100)

	def __str__(self):
		return self.name