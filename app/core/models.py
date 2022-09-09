"""
Database models.
"""
# import uuid
# import os
from decimal import Decimal

# from location_field.models.plain import PlainLocationField

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Validators for adherence field
PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

SEX_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
]

# User creation and Management ---------

# Handles user and superuser management and creation.


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Creates, saves and returns a new user."""
        if not email:
            raise ValueError("User must have an email address.")
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
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    signup_time = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    # birth_date = models.DateField(default=None, blank=True, null=True)

    # city = models.CharField(max_length=255)
    # location = PlainLocationField(based_fields=['city'],
    #                               initial='4.712520,-74.045487')
    sex = models.CharField(max_length=30, choices=SEX_CHOICES)

    available_workout_days = models.CharField(max_length=10)
    # meals_per_day = models.PositiveSmallIntegerField()

    objects = UserManager()

    USERNAME_FIELD = "email"


class ProgramType(models.Model):
    """
    Programs available
    """

    id = models.AutoField(primary_key=True)
    program_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=30, choices=SEX_CHOICES)
    available_workout_days = models.CharField(max_length=10)


class ProgramTypeUser(models.Model):
    """
    Bridge between user and programs
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    program_type = models.ForeignKey(ProgramType, on_delete=models.CASCADE)


# User measurements ---------

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


# User's food and nutrition ---------

class NutritionalHistory(models.Model):
    """Stores nutritional values history."""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date = models.DateField(auto_now=True)
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
    name = models.CharField(max_length=255)
    enter_by = models.CharField(max_length=5)
    brand = models.CharField(max_length=255)
    type = models.CharField(max_length=30)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2)
    proteins = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)
    fibers = models.DecimalField(max_digits=5, decimal_places=2)
    sodium = models.DecimalField(max_digits=5, decimal_places=2)
    calories = models.DecimalField(max_digits=5, decimal_places=2)


class Ingestion(models.Model):
    """
    Defines ingestion history records for a user
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now=True)
    meal_number = models.PositiveSmallIntegerField()
    value = models.DecimalField(max_digits=5, decimal_places=2)


class FoodIngestion(models.Model):
    """
    Defines a bridge table relationship between Food and ingestion table
    """
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE)
    ingestion_id = models.ForeignKey(Ingestion, on_delete=models.CASCADE)


class NutritionHistory(models.Model):
    """
    Defines nutrition history records for a user
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now=True)
    carbohydrates_real = models.DecimalField(max_digits=5, decimal_places=2)
    proteins_real = models.DecimalField(max_digits=5, decimal_places=2)
    fats_real = models.DecimalField(max_digits=5, decimal_places=2)
    fibers_real = models.DecimalField(max_digits=5, decimal_places=2)
    sodium_real = models.DecimalField(max_digits=5, decimal_places=2)
    calories_real = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrates_goal = models.DecimalField(max_digits=5, decimal_places=2)
    proteins_goal = models.DecimalField(max_digits=5, decimal_places=2)
    fats_goal = models.DecimalField(max_digits=5, decimal_places=2)
    fibers_goal = models.DecimalField(max_digits=5, decimal_places=2)
    sodium_goal = models.DecimalField(max_digits=5, decimal_places=2)
    calories_goal = models.DecimalField(max_digits=5, decimal_places=2)
    adherence = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=Decimal(0),
        validators=PERCENTAGE_VALIDATOR,
    )


# Workout data ---------

class Workouts(models.Model):
    """
    Workouts available
    """
    id = models.AutoField(primary_key=True)
    workout_type = models.CharField(max_length=255)
    program_type_id = models.IntegerField(blank=True, null=True)


class Exercises(models.Model):
    """
    Different types of exercises to perform
    """
    id = models.AutoField(primary_key=True)
    exercise_name = models.CharField(max_length=255)
    target_muscle = models.CharField(max_length=255)
    workout_type = models.CharField(max_length=255)
    video_link = models.CharField(max_length=255)
    # FileField class FileField(upload_to='',
    # storage=None, max_length=100, **options)


class WorkoutHistory(models.Model):
    """
    Collects Workout history records for a user
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    adherence = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=Decimal(0),
        validators=PERCENTAGE_VALIDATOR,
    )


class ExerciseHistory(models.Model):
    """
    Collects exercise history records for a user
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    exercise_name = models.CharField(max_length=255)
    reps_real = models.IntegerField(blank=True, null=True)
    weight_real = models.IntegerField(blank=True, null=True)
    rest_real = models.IntegerField(blank=True, null=True)
    duration_real = models.IntegerField(blank=True, null=True)
    reps_goal = models.IntegerField(blank=True, null=True)
    weight_goal = models.IntegerField(blank=True, null=True)
    rest_goal = models.IntegerField(blank=True, null=True)
    duration_goal = models.IntegerField(blank=True, null=True)
    adherence = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=Decimal(0),
        validators=PERCENTAGE_VALIDATOR,
    )


class ExerciseWorkoutHistory(models.Model):
    """
    Bridge between exercise and workout history
    """
    exercise_history_id = models.ForeignKey(
                                    ExerciseHistory,
                                    on_delete=models.CASCADE,
                                )
    workout_history_id = models.ForeignKey(
                                    WorkoutHistory,
                                    on_delete=models.CASCADE,
                                    )


# Evaluation section ---------
class Question(models.Model):
    """
    Workout evaluation history
    """
    id = models.AutoField(primary_key=True)
    question_name = models.CharField(max_length=255)
    question_type = models.CharField(max_length=255)


class WorkoutEvalHistory(models.Model):
    """
    Workout evaluation history
    """
    id = models.AutoField(primary_key=True)
    workout_id = models.ForeignKey(Workouts, on_delete=models.CASCADE)


class EvaluationQuestion(models.Model):
    """
    LIst of questions and score
    """
    # where does evaluation id come from?
    id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    score = models.IntegerField(blank=True, null=True)


class SleepQuestion(models.Model):
    """
    Sleep questions
    """
    # is this the right id...
    id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    score = models.IntegerField(blank=True, null=True)


class SleepHistory(models.Model):
    """
    Sleep history
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    sleep_question_id = models.ForeignKey(
                            SleepQuestion,
                            on_delete=models.CASCADE,
                        )
    date = models.DateField(auto_now=True)
    score = models.IntegerField(blank=True, null=True)
