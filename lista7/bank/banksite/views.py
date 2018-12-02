from django.shortcuts import render, redirect,reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db import connection
import simplejson
from .models import Payment
from .forms import PaymentValidationForm
from .tables import HistoryTable
from django_tables2 import RequestConfig
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
	return render(request, 'banksite/home.html')

@staff_member_required
def awaiting_payments(request):
	context = {
		'payments': Payment.objects.filter(confirmed=False).values()
	}
	if request.method == 'POST':
		reqid = request.POST.get('button')
		query = (Payment.objects.filter(id=reqid).values())
		query.update(confirmed=True)
	return render(request, 'banksite/awaiting_payments.html', context)

@login_required
def payments(request):
	context = {
		'payments': Payment.objects.filter(sender=request.user).values()
	}
	return render(request, 'banksite/payments.html',context)

@login_required
def payment_summary(request):
	if request.session.get('status') == 'confirmed' :
		del request.session['status']
		data = {"title": request.session['title'], "content":request.session['content'], \
		"value": request.session['value'], "account":request.session['account']}
		return render(request,"banksite/payment-summary.html",data)

	else:
		return redirect(request,'banksite-payment')


@login_required
def payment_confirm(request):
	if request.method == 'POST':
		confirmation = request.POST.get('confirmed')
		title = request.POST.get('title')
		content = request.POST.get('content')
		value = request.POST.get('value')
		account = request.POST.get('account')
		payment = Payment(title = title, content = content,\
		value = value, sender = request.user, account = account,confirmed=confirmation)
		payment.save()
		request.session['status'] = 'confirmed'
		request.session['title'] = payment.title
		request.session['content'] = payment.content
		request.session['value'] = payment.value
		request.session['account'] = payment.account
		return redirect('banksite-payment-summary')

	if request.session.get('status') == 'posted':
		del request.session['status']
		data = {"title": request.session['title'], "content":request.session['content'], \
		"value": request.session['value'], "account":request.session['account']}
		return render(request,"banksite/payment-confirm.html",data)

	else:
		return redirect('banksite-payment')


@login_required
def payment(request):
	if request.method == 'POST':
		if request.POST.get('confirmation') == 'false':
			form = PaymentValidationForm(request.POST)
			if form.is_valid():
				payment = form.save(commit=False)
				request.session['title'] = payment.title
				request.session['content'] = payment.content
				request.session['value'] = payment.value
				request.session['account'] = payment.account
				request.session['status'] = 'posted'
				return redirect('banksite-payment-confirm')
			else:
				return render(request, 'banksite/payment.html', {'form':form})
	else:
		form = PaymentValidationForm()
		return render(request, 'banksite/payment.html', {'form': form})



@login_required(login_url='/login/')
def find_payment(request):
    if request.method == 'POST':
        user = request.user.id
        account = request.POST.get('account').split(";")
        query = "SELECT * FROM banksite_payment WHERE banksite_payment.sender_id={} AND banksite_payment.account={}".format(user,account[0])
        model_items = Payment.objects.raw(query)

        for i in range(1, len(account)):
            q = account[i]
            cursor = connection.cursor()
            cursor.execute(q)

    else:
        model_items = Payment.objects.filter(sender=request.user)

    history_table = HistoryTable(model_items)
    RequestConfig(request).configure(history_table)
    return render(request, 'banksite/find_payment.html', {'history_table': history_table})
