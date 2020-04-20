from django.conf import settings
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Item, OrderItem, Order, BillingAddress, Payment
from django.views.generic import (
	ListView, 
	DetailView, 
	View, 
	TemplateView,
	CreateView,
	DeleteView,
	UpdateView
	)
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .blog_forms import CheckoutForm
from django.shortcuts import redirect
from itertools import chain
from users.models import Profile
from django.contrib.auth.models import User


import stripe
stripe.api_key = settings.STRIPE_SECRETE_KEY

class CheckoutView(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			form = CheckoutForm()
			context ={
			'form':form,
			'order':order,
			}
			return render(self.request, "blogs/checkout.html", context)
		except ObjectDoesNotExist:
			messages.error(self.request,f"No active orders available")
			return redirect("blogs:checkout")

	def post(self, *args, **kwargs):
		form = CheckoutForm(self.request.POST or None)
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			
			if form.is_valid():
				street_address    = form.cleaned_data.get('street_address')
				apartment_address = form.cleaned_data.get('apartment_address')
				country           = form.cleaned_data.get('country')
				zip               = form.cleaned_data.get('zip')
				#TODO: will add functionality later 
				# same_biling_address=form.cleaned_data.get('same_biling_address')
				# save_info=form.cleaned_data.get('save_info')
				payment_option = form.cleaned_data.get('payment_options')
				billing_address = BillingAddress(
					user              = self.request.user,
					street_address    = street_address,
					apartment_address = apartment_address,
					country           = country,
					zip               = zip
					)
				billing_address.user=self.request.user
				billing_address.save()
				order.billing_address = billing_address
				order.save()
				if payment_option  =='P':
					return redirect("payment:payment_process" )
				elif payment_option =='S':
					return redirect("blogs:payment_option", payment_option="Stripe" )
			else:
				return redirect("blogs:checkout")
		except ObjectDoesNotExist:
			messages.error(self.request, f"No active orders available")
			return redirect(self.request, "blogs:order_summary")

# class PaymentView(View):
# 	def get(self, *args, **kwargs):
# 		order = Order.objects.get(user=self.request.user, ordered=False)
# 		context={'order':order}
# 		return render(self.request, "blogs/payment_option.html", context)

	# def post(self, *args, **kwargs):
	# 	order = Order.objects.get(user=self.request.user, ordered=False)
	# 	token = self.request.POST.get('stripe-token-handler')
	# 	amount=int(order.get_total()*100)
	# 	try:
	# 		charge=stripe.Charge.create(
	# 		amount=amount,
	# 		currency="gbp",
	# 		source="token", 
	# 		)
	# 		payement=Payment()
	# 		payment.stripe_charge_id=charge['id']
	# 		payment.user=self.request.user
	# 		payment.amount =order.get_total()
	# 		payment.save()

			# order_item =order.items.all()
			# order_item.update(ordered=True)
			# order.ordered=True
			# order.payment=payment
			# order.save()

	# 		messages.success("Your purchase was successfull")
	# 		return redirect("/")

		# except stripe.error.CardError as err:
		# 	body = e.json_body
		# 	err = body.get('error', {})
		# 	messages.error(self.request, f"card eror") 
		# except stripe.error.RateLimitError as err:
		#   # Too many requests made to the API too quickly
		#   messages.error(self.request, "Rate limit error") 
		# except stripe.error.InvalidRequestError as err:
		#   # Invalid parameters were supplied to Stripe's API
		#   messages.error(self.request, f"") 
		# except stripe.error.AuthenticationError as err:
		#   # Authentication with Stripe's API failed
		#   # (maybe you changed API keys recently)
		#   messages.error(self.request, f"") 
		# except stripe.error.APIConnectionError as err:
		#   # Network communication with Stripe failed
		#   messages.error(self.request, f"") 
		# except stripe.error.StripeError as err:
		#   # Display a very generic error to the user, and maybe send
		#   # yourself an email
		#   messages.error(self.request, f"") 
		# except Exception as err:
		#   # Something else happened, completely unrelated to Stripe
		#   messages.error(self.request, f"") 
		
 
def products(request):
	context={
		'items':Item.objects.all().order_by('-date')
	}
	return render(request, 'blogs/product.html', context)

class HomeView(ListView):
	model = Item
	paginate_by=20
	template_name = "blogs/home.html"

class OrderSummaryView(LoginRequiredMixin,View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			context = {
			'object': order
			}
			return render(self.request, "blogs/order_summary.html", context)
			# return render(self.request, "blogs/checkout.html", context)
		except ObjectDoesNotExist:
			messages.info(self.request, "You have no items in your cart you can add items here")
			return redirect("/")
		

class ItemDetailView(DetailView):
	model = Item
	template_name = 'blogs/product.html'

@login_required
def add_to_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_item, created= OrderItem.objects.get_or_create(
		item=item,
		user = request.user,
		ordered =False
		)
	order_qs= Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# check if the order is in the ordered items
		if order.items.filter(item__slug = item.slug).exists():
			order_item.quantity += 1
			order_item.save()
		else:
			order.items.add(order_item)

	else:
		ordered_date =timezone.now()
		order = Order.objects.create(user = request.user,ordered_date=ordered_date)
		order.items.add(order_item)
	return redirect( "blogs:order_summary")
	
#this method remove item from cart
def remove_from_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_qs= Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# check if the order is in the ordered items
		if order.items.filter(item__slug = item.slug).exists():
			order_item  = OrderItem.objects.filter(
				item    = item,
				user    = request.user,
				ordered =False
		        )[0]
			order.items.remove(order_item)
		else:
			messages.info(request, "Item remove successfully")
			return redirect("blogs:order_summary")
	else:
		messages.info(request, "You do not have items in your cart")
		return redirect("blogs:order_summary")

	return redirect("blogs:order_summary")

def remove_single_item_from_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_qs= Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# check if the order is in the ordered items
		if order.items.filter(item__slug = item.slug).exists():
			order_item= OrderItem.objects.filter(
				item=item,
				user = request.user,
				ordered =False
		        )[0]
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
			else:
				order.items.remove(order_item)
		else:
			messages.info(request, "Item quantity updated")
			return redirect("blogs:order_summary")
	else:
		messages.info(request, "You do not have items in your cart")
		return redirect("blogs:order_summary")

	return redirect("blogs:order_summary")

#TODO: creat a method to search for items in the website
class SearchView(ListView):
    template_name = 'blogs/search_items.html'
    paginate_by = 20
    count = 0
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        
        if query is not None:
        	return Item.objects.search(query=query)
            # product_results        = Item.objects.search(query)
            # # lesson_results      = Lesson.objects.search(query)
            # # profile_results     = Profile.objects.search(query)
            
            # # combine querysets 
            # queryset_chain = chain(
            #         product_results ,
            #         # lesson_results,
            #         # profile_results
            # )        
            # qs = sorted(queryset_chain, 
            #             key=lambda instance: instance.pk, 
            #             reverse=True)
            # self.count = len(qs) # since qs is actually a list
            # return qs
        return Item.objects.none() 

class CategoryView(ListView):
	model         = Item
	paginate_by   =20
	template_name = 'blogs/category_view.html'
	
class DashboardView(LoginRequiredMixin, View):
	def get(self,request, *args, **kwargs):
		profile = Profile.objects.get(user=self.request.user)
		items = Item.objects.filter(owner=self.request.user)
		context={
		'profile':profile,
		'items':items
		}

		return render(request, 'blogs/dashboard.html', context)

	def post(self, *args, **kwargs):
		pass


class ItemAploadView(LoginRequiredMixin, CreateView):
	model = Item 
	fields = ['title','price',
				'category','label','image',
					'description']
	template_name= 'blogs/aplaoditem.html'

	def form_valid(self, form):
		form.instance.owner=self.request.user
		return super().form_valid(form)

class ItemDeleteView(UserPassesTestMixin,LoginRequiredMixin, DeleteView):
	model = Item
	template_name="blogs/delete.html"
	success_url='/'

	def test_func(self):
		item = self.get_object()
		if self.request.user == item.owner:
			return True
		return False

class ItemUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Item
	fields =['title', 'price', 'discount_price', 'description']
	template_name = 'blogs/itemUpdate.html'

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)


	def test_func(self):
		item = self.get_object()
		if self.request.user ==item.owner:
			return True
		return False

	