from .models import Item, Order, OrderItem
from rest_framework import serializers



class ItemViewSerilizer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields=('title','price','discount_price',
			'category','label','image','description')
		