from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

    def __unicode__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    telephone = models.BigIntegerField()
    # email = models.CharField(max_length=60)
    email = models.EmailField()
    address = models.CharField(max_length=100)

    def __unicode__(self):
        return self.username

class Book(models.Model):
    bookname = models.CharField(max_length=255)
    author = models.CharField(max_length=60)
    press = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # price = models.FloatField(max_digits=6, decimal_places=2)
    sum_quantity = models.IntegerField()

    def __unicode__(self):
        return self.bookname

class Order(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    quantity = models.IntegerField(default='1')


