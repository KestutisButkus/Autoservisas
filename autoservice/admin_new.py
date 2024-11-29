from django.contrib import admin
from .models import CarModel, Car, Order, Service, OrderLine

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline]
    list_display = ("id", 'car', 'date')

    # list_display = ('id', 'date', 'status', 'car')


class CarAdmin(admin.ModelAdmin):
    list_display = ('customer', 'car_model', 'car_num', 'vin_code')
    list_filter = ('customer', 'car_model')
    search_fields = ('car_num', 'vin_code')
    search_help_text = 'Paieška pagal valstybinį numerį, arba VIN kodą'

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'price')

class OrderLineViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'car_num', 'car_model', 'service_name', 'amount', 'date')
    list_filter = ('customer', 'car_model')
    # search_fields = ('car_num', 'vin_code')
    # search_help_text = 'Paieška pagal valstybinį numerį, arba VIN kodą'

admin.site.register(Car, CarAdmin)
admin.site.register(CarModel)
admin.site.register(Order, OrderAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderLine, OrderLineViewAdmin)