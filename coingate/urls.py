from django.urls import path
from coingate import views

urlpatterns = [
    path('', views.PaymentView.as_view(), name='payment-button'),
    path('create_payment', views.CreatePaymentView.as_view(), name='create-payment'),

    # path('all_payments', views.PaymentListView.as_view(), name='all'),
    path('all_payments', views.PaymentListApiView.as_view(), name='all'),

]
