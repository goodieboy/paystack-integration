from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PaymentForm
from django.conf import settings
from .models import Payment
from django.contrib import messages
from account.models import User


# Create your views here.
def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, 'make_payment.html', {'payment': payment,
                                                         'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = PaymentForm()
    return render(request, 'initiate_payment.html', {'payment_form': payment_form})


def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Verification Successful')
    else:
        messages.error(request, 'Verification Failed')
    return redirect('initiate_payment')


def test(request):
    user = User.objects.all()
    return render(request, 'test.html', {'user': user})
