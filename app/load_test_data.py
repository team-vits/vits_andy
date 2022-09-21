from xxlimited import foo
from core.models import (
    AnthropometricHistory,
    Food,
    Ingestion,
    IngestionByFood,
    Exercise,
    NutritionalHistory,
    ProgramType,
    Workout,
)
from django.contrib.auth import get_user_model
from faker import Faker
import random
import math
from datetime import date, datetime

# Activity levels
SEDENTARY = 1.2
MODERATE = 1.37
ACTIVE = 1.5


# Constant factors to calculate BMR
SEX_FACTOR = {
    "M": 1,
    "F": 0,
}

PROGRAMS = ["lose weight", "gain weight"]

fake = Faker()


def create_client():
    """Create a fake data client"""
    client = fake.simple_profile()
    client_data = {
        "name": client["name"],
        "email": client["mail"],
        "birth_date": client["birthdate"].isoformat(),
        "city": fake.city(),
        "sex": client["sex"],
        "meals_per_day": fake.random_int(min=2, max=5),
        "password": fake.pystr(max_chars=8),
        "available_workout_days": "".join(
            fake.random_sample(elements=("1", "2", "3", "4", "5", "6", "7"), length=4)
        ),
        "activity_level": random.choice([SEDENTARY, MODERATE, ACTIVE]),
    }
    return client_data


def create_anthropometric(user):
    """Create anthropometric data and save it in database"""
    anthropometric_history = {
        "user": user,
        "height": round(random.uniform(150, 200), 1),
        "weight": round(random.uniform(50.0, 120.0), 1),
        "neck": round(random.uniform(25.0, 60.0), 1),
        "waist": round(random.uniform(60.0, 100.0), 1),
    }
    anthropometric_history["hip"] = (
        round(anthropometric_history["waist"] / random.uniform(0.70, 0.96)) / 1
    )
    AnthropometricHistory.objects.create(**anthropometric_history)


def create_workouts():
    """Create random workouts with exercises"""
    exercises = Exercise.objects.all()
    workout_type = "strenght"
    for i in range(10):
        exercises_per_workout = random.choices(exercises, k=3)
        workout = Workout.objects.create(workout_type=workout_type)
        workout.exercises.set(exercises_per_workout)


def subscribe_user_to_program(user):
    """Add a new user to a program and define workouts"""
    workouts = Workout.objects.all()
    workouts_per_program = random.choices(workouts, k=5)
    p = ProgramType.objects.create(
        program_name=random.choice(PROGRAMS), sex=user.sex, user=user
    )
    p.workouts.set(workouts_per_program)


def create_user(client_data):
    """Create user data and save it in database"""
    User = get_user_model()
    user = User.objects.create_user(
        email=client_data["email"], password=client_data["password"]
    )
    for key, value in client_data.items():
        if key != "password" and key != "email":
            setattr(user, key, value)
    user.save()
    return user


def create_ingestion_of_one_day(user):
    """Create 3 ingestions with diferent foods for a user"""
    foods = Food.objects.all()

    # One day of a user eating
    for meal in range(1, user.meals_per_day + 1):
        ingestion = Ingestion.objects.create(user=user, meal_number=meal)
        food_list = random.choices(foods, k=3)
        for food in food_list:
            IngestionByFood.objects.create(
                ingestion=ingestion, food=food, value=round(random.uniform(10, 100), 1)
            )


def calculate_nutritional_data(user):
    """Calculate all the nutriotional values from the ingestions"""
    user_weight = user.anthropometrics.latest("date").weight

    # Calculate BMR
    BF_kilo = user.get_body_fat()
    FFM_kilo = user_weight - BF_kilo
    FM_kilo = user_weight - FFM_kilo

    age = user.get_age()

    BMR = (
        (13.587 * FFM_kilo)
        + (9.613 * FM_kilo)
        + (198 * SEX_FACTOR[user.sex])
        - (3.351 * age)
        + 674
    )

    # Calculate calories
    calories_goal_per_day = BMR * user.activity_level

    # Calculate goal macro nutrients goals
    nutrition_goals = {}
    if user.program_types == "lose_weight":
        proteins_goal = FFM_kilo * 2.5
    else:
        proteins_goal = FFM_kilo * 2
    nutrition_goals["proteins_goal"] = proteins_goal
    nutrition_goals["fats_goal"] = (calories_goal_per_day - (proteins_goal * 4)) * (
        0.35 / 9
    )
    nutrition_goals["carbohydrates_goal"] = (
        calories_goal_per_day - (proteins_goal * 4)
    ) * (0.65 / 4)
    nutrition_goals["fibers_goal"] = calories_goal_per_day * (13 / 1000)

    # Calculate real macro nutrients real per meal and total per day
    ingestions_one_day = Ingestion.objects.filter(user=user)
    proteins_total_real = 0
    fats_total_real = 0
    carbohydrates_total_real = 0
    fiber_total_real = 0
    calories_total_real = 0
    for ingestion in ingestions_one_day:
        foods_by_ingestion = IngestionByFood.objects.filter(ingestion=ingestion)
        for food in foods_by_ingestion:
            food_nutrients = Food.objects.get(name=food.food.name)
            protein_real = food.value * (food_nutrients.proteins / 100)
            fat_real = food.value * (food_nutrients.fats / 100)
            carbohydrate_real = food.value * (food_nutrients.carbohydrates / 100)
            fiber_real = food.value * (food_nutrients.fibers / 100)
            calories = food.value * (food_nutrients.calories / 100)
        proteins_total_real += protein_real
        fats_total_real += fat_real
        carbohydrates_total_real += carbohydrate_real
        fiber_total_real += fiber_real
        calories_total_real += calories

    nutrition_reals = {
        "proteins_real": proteins_total_real,
        "fats_real": fats_total_real,
        "carbohydrates_real": carbohydrates_total_real,
        "fibers_real": fiber_total_real,
    }

    NutritionalHistory.objects.create(
        **nutrition_goals,
        **nutrition_reals,
        user=user,
        calories_goal=calories_goal_per_day,
        calories_real=calories_total_real
    )


def main():
    """Start the program"""

    # Create workout
    create_workouts()

    # User's creation
    client_data = create_client()
    user = create_user(client_data)

    # Add user to a program
    subscribe_user_to_program(user)

    # User's anthropometric data
    create_anthropometric(user)

    # User's ingestion
    create_ingestion_of_one_day(user)

    # Get nutrional data accoring the ingestions
    calculate_nutritional_data(user)


# Start the program
main()
