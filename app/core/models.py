"""
Database models.
"""
# import uuid
# import os
from decimal import Decimal
from datetime import datetime, date
import math

# from location_field.models.plain import PlainLocationField

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Variable for Macronutrients settings
MACRO_FIELDS = {"max_digits": 4, "decimal_places": 1, "default": Decimal(0.0)}

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
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
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
    # Activity level
    SEDENTARY = 1.2
    MODERATE = 1.37
    ACTIVE = 1.5
    ACTIVITY_LEVEL = [
        (SEDENTARY, 'Sedentary'),
        (MODERATE, 'Moderate'),
        (ACTIVE, 'Active'),
    ]

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    signup_time = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateField(default=None, blank=True, null=True)

    city = models.CharField(max_length=255)
    # location = PlainLocationField(based_fields=['city'],
    #                               initial='4.712520,-74.045487')
    sex = models.CharField(max_length=30, choices=SEX_CHOICES)

    available_workout_days = models.CharField(max_length=10)
    activity_level = models.FloatField(choices=ACTIVITY_LEVEL, null=True)
    meals_per_day = models.PositiveSmallIntegerField(null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"


    def get_age(self):
        """Calculate age of the user"""

        today = date.today()
        birthdate_object = datetime.strptime(self.birth_date, '%Y-%m-%d').date()
        age = today.year - birthdate_object.year - ((today.month, today.day) < (birthdate_object.month, birthdate_object.day))
        return age

    def get_body_fat(self):
        """Get body fat of the user in kilograms"""
        user_anthropometrics = self.anthropometrics.latest('date')
        if self.sex == 'M':
            BF_percent = (
                495
                / (
                    1.0324
                    - 0.19077 * math.log10(user_anthropometrics.waist - user_anthropometrics.neck)
                    + 0.15456 * math.log10(user_anthropometrics.height)
                )
            ) - 450
        else:
            BF_percent = (
            495
            / (
                1.29579
                - 0.35004 * math.log10(user_anthropometrics.waist + user_anthropometrics.hip - user_anthropometrics.neck)
                + 0.22100 * math.log10(user_anthropometrics.height)
            )
        ) - 450
        return BF_percent * user_anthropometrics.weight


# User measurements ---------
class AnthropometricHistory(models.Model):
    """
    Defines Antrhopometric history records for a user
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="anthropometrics"
    )
    date = models.DateField(auto_now_add=True)
    height = models.FloatField()
    weight = models.FloatField()
    neck = models.FloatField()
    waist = models.FloatField()
    hip = models.FloatField()


# User's food and nutrition ---------
class NutritionalHistory(models.Model):
    """Stores nutritional values history."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="nutritional_histories"
    )
    date = models.DateField(auto_now_add=True)
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


class Food(models.Model):
    """Defines nutritional values of food."""

    name = models.CharField(max_length=255)
    enter_by = models.CharField(max_length=5)
    brand = models.CharField(max_length=255)
    type = models.CharField(max_length=30)
    carbohydrates = models.DecimalField(**MACRO_FIELDS)
    proteins = models.DecimalField(**MACRO_FIELDS)
    fats = models.DecimalField(**MACRO_FIELDS)
    fibers = models.DecimalField(**MACRO_FIELDS)
    sodium = models.DecimalField(**MACRO_FIELDS)
    calories = models.DecimalField(**MACRO_FIELDS)


class Ingestion(models.Model):
    """
    Defines ingestion history records for a user
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ingestions")
    date = models.DateTimeField(auto_now_add=True)
    meal_number = models.PositiveSmallIntegerField()

class IngestionByFood(models.Model):
    ingestion = models.ForeignKey(Ingestion, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)


# Workout data ---------
class Exercise(models.Model):
    """
    Different types of exercises to perform
    """

    exercise_name = models.CharField(max_length=255)
    target_muscle = models.CharField(max_length=255)
    workout_type = models.CharField(max_length=255)
    video_link = models.CharField(max_length=255, default="")
    # FileField class FileField(upload_to='',
    # storage=None, max_length=100, **options)


class Workout(models.Model):
    """
    Workouts available
    """

    workout_type = models.CharField(max_length=255)
    exercises = models.ManyToManyField(Exercise, related_name="workouts")


class ProgramType(models.Model):
    """
    Programs available
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="program_types", null=True
    )
    workouts = models.ManyToManyField(
        Workout,
        related_name="programs",
    )
    program_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=30, choices=SEX_CHOICES)
    #available_workout_days = models.CharField(max_length=10)


class StrengthHistory(models.Model):
    """
    Collects exercise history records for a user
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sleep_histories"
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


class CardioHistory(models.Model):
    """
    Collects exercise history records for a user
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cardio_histories"
    )
    exercise_name = models.CharField(max_length=255)
    duration_real = models.IntegerField(blank=True, null=True)
    active_rest_real = models.IntegerField(blank=True, null=True)
    cicle_real = models.IntegerField(blank=True, null=True)
    sprint_real = models.IntegerField(blank=True, null=True)
    min_bpm_real = models.IntegerField(blank=True, null=True)
    max_bpm_real = models.IntegerField(blank=True, null=True)
    duration_goal = models.IntegerField(blank=True, null=True)
    active_rest_goal = models.IntegerField(blank=True, null=True)
    cicle_goal = models.IntegerField(blank=True, null=True)
    sprint_goal = models.IntegerField(blank=True, null=True)
    min_bpm_goal = models.IntegerField(blank=True, null=True)
    max_bpm_goal = models.IntegerField(blank=True, null=True)


class WorkoutHistory(models.Model):
    """
    Collects Workout history records for a user
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="workout_histories"
    )
    strength_exercises = models.ManyToManyField(StrengthHistory)
    cardio_exercises = models.ManyToManyField(CardioHistory)


# Evaluation section ---------
class Question(models.Model):
    """
    Workout evaluation history
    """

    question = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    frequency = models.CharField(max_length=255)
    scale_name = models.CharField(max_length=255)


class WorkoutQuestionHistory(models.Model):
    """
    LIst of questions and score
    """

    questions = models.ManyToManyField(
        Question, related_name="workout_question_histories"
    )
    date = models.DateField(auto_now_add=True)
    score = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="workout_questions",
    )
    workouts = models.ManyToManyField(
        Workout,
    )


class SleepQuestionHistory(models.Model):
    """
    Sleep questions
    """

    questions = models.ManyToManyField(
        Question, related_name="sleep_question_histories"
    )
    date = models.DateField(auto_now_add=True)
    score = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sleep_questions",
    )
