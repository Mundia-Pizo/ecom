from django.urls import path
from .views import (products, 
	 CheckoutView,
	 HomeView, 
	 ItemDetailView, 
	 add_to_cart,
	 remove_from_cart,
	 OrderSummaryView,
	 remove_single_item_from_cart,
	 # PaymentView,
	 CategoryView, 
	 SearchView,
	 DashboardView,
	 ItemAploadView

	  )

app_name = 'blogs'

urlpatterns = [
	path('', HomeView.as_view(), name ="home" ),
	path('checkout/', CheckoutView.as_view(), name = "checkout" ),
	# path('payment_option/<payment_option>/', PaymentView.as_view(), name = "payment_option" ),
	path('order_summary/', OrderSummaryView.as_view(), name = "order_summary" ),
	path('search/', SearchView.as_view(), name = "search" ),
	path('products/<slug>/',ItemDetailView.as_view(), name = "products" ),
	path('add_to_cart/<slug>/',add_to_cart, name="add_to_cart"),
	path('remove_from_cart/<slug>/',remove_from_cart, name="remove_from_cart"),
	path('remove_single_item_from_cart/<slug>/',remove_single_item_from_cart,
	                                name="remove_single_item_from_cart"),
	path('category/', CategoryView.as_view(), name = "category" ),
	path('dashboard/', DashboardView.as_view(), name='dashboard'),
	path('appload/', ItemAploadView.as_view(), name='appload')

]