from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.car_list, name='cars'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('orders/', views.OrderListView.as_view(), name='object_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('search/', views.search, name='search'),
    path('mycars/', views.CarByUserView.as_view(), name='my-borrowed'),
    path('register/', views.register, name='register')
]
