from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.car_list, name='cars'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('orders/', views.OrderListView.as_view(), name='object_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('search/', views.search, name='search'),
    path('mycars/', views.CarByUserView.as_view(), name='my-borrowed'),
    path('mycars/<int:pk>', views.CarByUserDetailView.as_view(), name='my_car'),
    path('mycars/new', views.CarByUserCreateView.as_view(), name='my-borrowed-new'),
    path('mycars/<int:pk>/update', views.CarByUserUpdateView.as_view(), name='my-car-update'),
    path('mycars/<int:pk>/delete', views.CarByUserDeleteView.as_view(), name='my-car-delete'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
    path('i18n/', include('django.conf.urls.i18n')),
]
