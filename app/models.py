import datetime

from django.db import models
from django.utils import timezone


class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()


class Client(models.Model):
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()


class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)


class Order(models.Model):
    products = models.ManyToManyField(Product, through='OrderProduct')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(default=timezone.now)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
