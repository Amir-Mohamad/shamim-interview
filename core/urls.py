from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('payments/', views.PaymentsView.as_view(), name='payments'),
    path('pay/<int:pk>/', views.PayView.as_view(), name='pay'),
]
