from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse 
from django_countries.fields import CountryField
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from django.db.models import Q

class ProductQuerySet(models.QuerySet):
	def search(self, query=None):
		qs = self
		if query is not None:
			or_lookup = (Q(title__icontains=query) | 
                         Q(description__icontains=query)|
                         Q(slug__icontains=query)|
                         Q(category__icontains=query)
                        )
			qs = qs.filter(or_lookup).distinct() 
		return qs

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def search(self, query=None):
		return self.get_queryset().search(query=query)

    


CATEGORY_CHOICES =(
     ('S','shirt'),
     ('SW','sport wear'),
     ('OS','out wear'),
     ('LW','Ladies watches'),
     ('MW','Mens watch'),
     ('MS', 'Mens Shoes'),
     ('PH', 'Smart Phones'),
     ('LP', 'Laptop')

	)

LABEL_CHOICES =(
     ('P','primary'),
     ('S','secondary'),
     ('D','danger'),
	)


class Item(models.Model):
	title           = models.CharField(max_length=100)
	price           = models.FloatField()
	discount_price  = models.FloatField(blank=True, null=True)
	category        = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
	label           = models.CharField(choices=LABEL_CHOICES, max_length=2)
	image           = models.ImageField(upload_to='product_pictures')
	slug            = models.SlugField()
	description     = models.TextField()
	objects         = ProductManager()

	# thumbnail = ImageSpecField(
	# 	source='image', processors=[ResizeToFit(200, 200)], format='PNG',options = {'quality': 200})

   ## overiding the model save method to save our images in the formt we want them to be
	def save(self):
		super().save()

		img = Image.open(self.image.path)

		if img.height > 250 or img.width>250:
			output_size =(250, 250)
			img.thumbnail(output_size)
			img.save(self.image.path)
		else:
			pass
	

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("blogs:products", kwargs={
			'slug': self.slug
			})
	def get_add_to_cart_url(self):
		return reverse("blogs:add_to_cart", kwargs={
			'slug': self.slug
			})
	def get_remove_from_cart_url(self):
		return reverse("blogs:remove_from_cart", kwargs={
			'slug': self.slug
			})

class  OrderItem(models.Model):
	user     = models.ForeignKey(settings.AUTH_USER_MODEL,
	                        on_delete=models.CASCADE)
	ordered  = models.BooleanField(default=False)
	item     = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	date     = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return  f"{self.quantity} of {self.item.title}"

	def get_item_total_price(self):
		return self.quantity * self.item.price

	def get_item_total_discount_price(self):
		return self.quantity * self.item.discount_price

	def get_amount_saved(self):
		return self.get_item_total_price() - self.get_item_total_discount_price()
	def get_final_price(self):
		if self.item.discount_price:
			return self.get_item_total_discount_price()
		return self.get_item_total_price()


	

class Order(models.Model):
	user           = models.ForeignKey(settings.AUTH_USER_MODEL,
	                        on_delete=models.CASCADE)
	items          = models.ManyToManyField(OrderItem)
	start_date     = models.DateTimeField(auto_now_add=True)
	ordered_date   = models.DateTimeField()
	ordered        = models.BooleanField(default=False)
	biling_address = models.ForeignKey("BillingAddress", 
		          on_delete=models.SET_NULL, blank=True, null=True)
	payment        = models.ForeignKey("Payment", 
		          on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.user.username
	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total +=order_item.get_final_price()
		return round(total,2)
	def get_shipping(self):
		shipping=0
		if self.get_total() <=10:
			shipping=self.get_total()*0.05
		elif self.get_total() >10 and self.get_total()<=20:
			shipping=self.get_total()*0.06

		elif self.get_total() >20 and self.get_total()<=100:
			shipping=self.get_total()*0.08
		# elif self.get_total() >50 and self.get_total()<=100:
		# 	shipping=self.get_total()*0.10
		else:
			shipping=self.get_total()*0.11
		return round(shipping,2)
	def get_total_and_shipping(self):
		return round((self.get_total() + self.get_shipping()),2)


class BillingAddress(models.Model):
	user              = models.ForeignKey(settings.AUTH_USER_MODEL,
	                        on_delete=models.CASCADE)
	street_address    = models.CharField(max_length=200)
	apartment_address = models.CharField(max_length=200)
	country           = CountryField(multiple=False)
	zip               = models.CharField(max_length=20)

	def __str__(self):
		return self.user.username


#keepin track of the payment

class Payment(models.Model):
	stripe_charge_id = models.CharField(max_length=40)
	user             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
	amount           = models.FloatField()
	timestamp        = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.user.username   
