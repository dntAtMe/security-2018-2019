from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are able to log in now.')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})

@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user,request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Password changed successfully !')
			return redirect('change_password')
		else:
			messages.error(request, 'Current password not valid !')
			return redirect('change_password')
	else:
		form = PasswordChangeForm(request.user)
		return render(request,'users/change_passwd.html',{'form': form})
