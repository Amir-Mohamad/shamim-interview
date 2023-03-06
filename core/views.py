from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Employee, Payment
from .forms import AddPaymentForm


class HomeView(View):
    template_name = 'core/home.html'

    def get(self, request):
        return render(request, self.template_name)


class DashboardView(LoginRequiredMixin, View):
    template_name = 'core/dashboard.html'
    form = AddPaymentForm

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form(request.POST, extra=request.POST['employee_count'])
        if form.is_valid():
            for i in range(0, 10):  # 10 is the maximum number of dynamic fields
                employee_name_field = f'employee_name_field_{i}'
                hour_field = f'hour_field_{i}'
                price_field = f'price_field_{i}'
                if employee_name_field and hour_field and price_field in form.cleaned_data:
                    cd = form.cleaned_data
                    employee = Employee.objects.create(
                        employer=request.user,
                        name=form.cleaned_data[employee_name_field],
                        hour=form.cleaned_data[hour_field],
                        price_for_each_hour=form.cleaned_data[price_field],
                    )
                    Payment.objects.create(
                        employer=request.user,
                        title=cd['title'],
                        date=cd['date'],
                        employee=employee, status='PG'
                    )
            messages.success(
                request, 'Your payment has been successfully registered', 'green')
            return redirect('core:dashboard')

        return render(request, 'accounts/register.html', {'form': form})


class PaymentsView(LoginRequiredMixin, View):
    template_name = 'core/payments.html'

    def get(self, request):
        payments = Payment.objects.filter(employer=request.user)
        return render(request, self.template_name, context={'payments': payments})


class PayView(LoginRequiredMixin, View):
    template_name = 'core/pay.html'

    def get(self, request, pk):
        payment = get_object_or_404(Payment, id=pk)
        if payment.status == 'DE':
            messages.error(
                request, 'You have already payed', 'red')
        elif payment.status == 'PG':
            budget = request.user.budget
            if payment.employee.total_salary > budget:
                messages.error(
                    request, 'Your budget isnt enougth', 'red')
            else:
                request.user.budget = request.user.budget - payment.employee.total_salary
                request.user.save()
                payment.status = 'DE'
                payment.save()
                messages.success(
                    request, 'Your payment has been successfully payed', 'green')
        return redirect('core:payments')
