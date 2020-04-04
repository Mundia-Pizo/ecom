from .views import payment_process, payment_done, payment_cancelled
from django.urls import path


app_name = 'payment'

urlpatterns = [
     path('', payment_process, name='payment_process'),
     path('done/', payment_done, name ='done'),
     path('payment_cancelled/', payment_cancelled, name='cancelled')
	]