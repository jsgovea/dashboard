from django.contrib import admin

# Register your models here.
from dashboardapp.models import Restaurant, Customer, Meal, Order, OrderDetail

admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(OrderDetail)