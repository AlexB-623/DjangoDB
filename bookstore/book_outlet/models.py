from dataclasses import replace
from tkinter.constants import CASCADE
from wsgiref.validate import validator
from django.db.models import Model
from django.urls import reverse
from django.db import models
from django.forms import CharField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Countries"


class Address(models.Model):
    street = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.postal_code}"

    class Meta:
        verbose_name_plural = "Address Entries"


# Create your models here.
class Author(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)

    def fullname(self):
        return f"{self.firstname} {self.lastname}"

    def __str__(self):
        return self.fullname()


class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name="books")
    is_bestselling = models.BooleanField(default=False)
    slug = models.SlugField(default="", blank=True, null=False)
    published_locales = models.ManyToManyField(Country)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} ({self.rating})"


