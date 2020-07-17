from blogs.models import Item,OrderItem, Order
from rest_framework import viewsets, permissions
from .serializers import ItemViewSerilizer


class ItemViewSet(viewsets.ModelViewSet):
	queryset = Item.objects.all()
	permission_classes=[
       permissions.AllowAny
	]
	serializer_class=ItemViewSerilizer