"""
Database models.
"""
import uuid
import os
from decimal import Decimal
#from location_field.models.plain import PlainLocationField

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

SEX_CHOICES = [
       ('M', 'Male'),
       ('F', 'Female'),
   ]

# Handles user and superuser management and creation.
class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Creates, saves and returns a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and returns a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=250, unique=True)
    name = models.CharField(max_length=250)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    signup_time = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    birth_date = models.DateField()

    # city = models.CharField(max_length=250)
    # location = PlainLocationField(based_fields=['city'],
    #                               initial='4.712520,-74.045487')
    # sex = models.CharField(max_length=30, choices=SEX_CHOICES)

    available_workout_days = models.CharField(max_length=10)
    meals_per_day = models.PositiveSmallIntegerField()

    objects = UserManager()

    USERNAME_FIELD = 'email'


class AntrhopometricHistory(models.Model):
    """
    Defines Antrhopometric history records for a user
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date = models.DateField(auto_now=True)
    height = models.FloatField()
    weight = models.FloatField()
    neck = models.FloatField()
    waist = models.FloatField()
    hip = models.FloatField()

class NutritionalHistory(models.Model):
    """Stores nutritional values history."""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date: models.DateField(auto_now=True)
    carbohydrates_real = models.IntegerField(blank=True, null=True)
    proteins_real = models.IntegerField(blank=True, null=True)
    fats_real = models.IntegerField(blank=True, null=True)
    fibers_real = models.IntegerField(blank=True, null=True)
    sodium_real = models.IntegerField(blank=True, null=True)
    calories_real = models.IntegerField(blank=True, null=True)
    carbohydrates_goal = models.IntegerField(blank=True, null=True)
    proteins_goal = models.IntegerField(blank=True, null=True)
    fats_goal = models.IntegerField(blank=True, null=True)
    fibers_goal = models.IntegerField(blank=True, null=True)
    sodium_goal = models.IntegerField(blank=True, null=True)
    calories_goal = models.IntegerField(blank=True, null=True)
    carbohydrates_goal = models.IntegerField(blank=True, null=True)

# Validators for adherence field
PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class Food(models.Model):
    """Defines nutritional values of food."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    enter_by = models.CharField(max_length=5)
    brand = models.CharField(max_length=250)
    type = models.CharField(max_length=30)
    carbohydrates = models.DecimalField(max_digits = 5, decimal_places = 2)
    proteins = models.DecimalField(max_digits = 5, decimal_places = 2)
    fats = models.DecimalField(max_digits = 5, decimal_places = 2)
    fibers = models.DecimalField(max_digits = 5, decimal_places = 2)
    sodium = models.DecimalField(max_digits = 5, decimal_places = 2)
    calories = models.DecimalField(max_digits = 5, decimal_places = 2)


class Food_Ingestion(models.Model):
    """
    Defines a bridge table relationship between Food and ingestion table
    """
    food_id = models.ForeignKey('Food', on_delete=models.CASCADE)
    ingestion_id = models.ForeignKey('Ingestion', on_delete=models.CASCADE)


class Ingestion(models.Model):
    """
    Defines ingestion history records for a user
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date =  models.DateTimeField(auto_now=True)
    meal_number = models.PositiveSmallIntegerField()
    value = models.DecimalField(max_digits = 5, decimal_places = 2)


class NutritionHistory(models.Model):
    """
    Defines nutrition history records for a user
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date =  models.DateTimeField(auto_now=True)
    carbohydrates_real = models.DecimalField(max_digits = 5, decimal_places = 2)
    proteins_real = models.DecimalField(max_digits = 5, decimal_places = 2)
    fats_real = models.DecimalField(max_digits = 5, decimal_places = 2)
    fibers_real = models.DecimalField(max_digits = 5, decimal_places = 2)
    sodium_real = models.DecimalField(max_digits = 5, decimal_places = 2)
    calories_real = models.DecimalField(max_digits = 5, decimal_places = 2)
    carbohydrates_goal = models.DecimalField(max_digits = 5, decimal_places = 2)
    proteins_goal = models.DecimalField(max_digits = 5, decimal_places = 2)
    fats_goal = models.DecimalField(max_digits = 5, decimal_places = 2)
    fibers_goal = models.DecimalField(max_digits = 5, decimal_places = 2)
    sodium_goal = models.DecimalField(max_digits = 5, decimal_places = 2)
    calories_goal = models.DecimalField(max_digits = 5, decimal_places = 2)
    adherence =  models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=Decimal(0),
        validators=PERCENTAGE_VALIDATOR
    )
