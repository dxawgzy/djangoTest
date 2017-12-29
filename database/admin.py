from django.contrib import admin

# Register your models here.

from database.models import Person
from database.models import User
from database.models import Book
from database.models import Order

admin.site.register(Person)

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Order)

