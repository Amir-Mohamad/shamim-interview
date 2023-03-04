from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin as message
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import views
from django.urls import reverse_lazy
from django.views import View
from .mixins import AuthenticatedMixin
from .forms import RegisterForm

User = get_user_model()


class RegisterView(View):
    success_url = reverse_lazy('core:home')

    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['email'], cd['password1'])
            messages.success(
                request, 'You have successfully registered - PEASE LOGIN TO SITE WITH YOUR EMAIL AND PASSWORD', 'success')
            return redirect('accounts:login')
        return render(request, 'accounts/register.html', {'form': form})


# Login user


class UserLogin(AuthenticatedMixin, message, views.LoginView):
    template_name = 'accounts/login.html'
    success_message = 'Login was successful'
    success_url = reverse_lazy('core:home')


# Logouting user
class UserLogout(views.LogoutView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are successfully logged out')
        return super().dispatch(request, *args, **kwargs)
