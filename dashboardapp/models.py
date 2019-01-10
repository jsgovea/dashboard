from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
RESTAURANT_CATEGORY = (
    ('d', 'Desayunos'),
    ('cr', 'Comida Rápida'),
    ('p', 'Postres')
)

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=RESTAURANT_CATEGORY)
    logo = models.ImageField(upload_to='restaurant_logo/', blank=False)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    avatar = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.user.get_full_name()


MEAL_CATEGORY = (
    ('d', 'Desayunos'),
    ('com', 'Comidas'),
    ('e', 'Entradas'),
    ('p', 'Postres'),
    ('c', 'Complementos'),
    ('b', 'Bebidas'),

)

class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    cook_time = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='meal_images/', blank=False)
    category = models.CharField(max_length=100, choices=MEAL_CATEGORY)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    Preparando = 1
    Listo = 2
    Entregado = 3

    STATUS_CHOICES = (
        (Preparando, "Preparando"),
        (Listo, "Listo"),
        (Entregado, "Entregado")
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    total = models.FloatField()
    status = models.IntegerField(choices = STATUS_CHOICES)
    created_at = models.DateTimeField(default = timezone.now)
    picked_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return str(self.id)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    extras = models.CharField(max_length=50, default="")
    comission = models.FloatField()
    sub_total = models.FloatField()

    def __str__(self):
        return str(self.id)
