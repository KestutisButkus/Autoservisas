from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('orders/', views.OrderListView.as_view(), name='object_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),  # Pridėta
]
