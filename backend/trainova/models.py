from django.contrib.auth.models import User
from django.db import models


class FitnessProfile(models.Model):
    GOAL_CHOICES = [
        ('fat_loss', 'Fat loss'), ('muscle_gain', 'Muscle gain'), ('strength', 'Strength'),
        ('endurance', 'Endurance'), ('general_fitness', 'General fitness'), ('rehab', 'Rehabilitation'),
    ]
    LEVEL_CHOICES = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]
    ACTIVITY_CHOICES = [('sedentary', 'Sedentary'), ('light', 'Light'), ('moderate', 'Moderate'), ('active', 'Active'), ('athlete', 'Athlete')]

    user = models.OneToOneField(User, related_name='fitness_profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=80, default='Nairobi')
    age = models.PositiveIntegerField(default=28)
    gender = models.CharField(max_length=40, blank=True)
    height_cm = models.FloatField(default=170)
    weight_kg = models.FloatField(default=70)
    target_weight_kg = models.FloatField(null=True, blank=True)
    goal = models.CharField(max_length=40, choices=GOAL_CHOICES, default='general_fitness')
    training_level = models.CharField(max_length=40, choices=LEVEL_CHOICES, default='beginner')
    activity_level = models.CharField(max_length=40, choices=ACTIVITY_CHOICES, default='moderate')
    weekly_target = models.PositiveIntegerField(default=4)
    available_equipment = models.CharField(max_length=255, default='Bodyweight, Dumbbells')
    injury_notes = models.TextField(blank=True)
    medical_clearance_confirmed = models.BooleanField(default=False)
    streak_days = models.PositiveIntegerField(default=0)
    readiness_status = models.CharField(max_length=40, default='Good')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.email or self.user.username


# Backward-compatible alias used by older seed/admin code names.
AppUser = FitnessProfile


class Exercise(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True)
    body_part = models.CharField(max_length=80)
    target_muscle = models.CharField(max_length=80)
    secondary_muscles = models.CharField(max_length=255, blank=True)
    equipment = models.CharField(max_length=80, default='Bodyweight')
    difficulty = models.CharField(max_length=40, default='Beginner')
    movement_pattern = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    safety_tips = models.TextField(blank=True)
    image = models.ImageField(upload_to='exercise_images/', blank=True, null=True)
    external_image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ExerciseAngleStandard(models.Model):
    exercise = models.ForeignKey(Exercise, related_name='angle_standards', on_delete=models.CASCADE)
    name = models.CharField(max_length=120, help_text='Example: Front knee angle, hip hinge angle')
    joint_a = models.CharField(max_length=80, help_text='First landmark name')
    joint_b = models.CharField(max_length=80, help_text='Middle/vertex landmark name')
    joint_c = models.CharField(max_length=80, help_text='Third landmark name')
    min_degrees = models.FloatField()
    max_degrees = models.FloatField()
    feedback_when_low = models.CharField(max_length=255, blank=True)
    feedback_when_high = models.CharField(max_length=255, blank=True)
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return f'{self.exercise.name} - {self.name}'


class ReferenceMedia(models.Model):
    exercise = models.ForeignKey(Exercise, related_name='references', on_delete=models.CASCADE)
    title = models.CharField(max_length=160)
    media_type = models.CharField(max_length=20, choices=[('image', 'Image'), ('video', 'Video')], default='image')
    file = models.FileField(upload_to='reference_media/', blank=True, null=True)
    external_url = models.URLField(blank=True)
    coaching_notes = models.TextField(blank=True)
    is_correct_form = models.BooleanField(default=True)
    landmark_data = models.JSONField(default=dict, blank=True)
    overlay_data = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class WorkoutPlan(models.Model):
    title = models.CharField(max_length=160)
    focus = models.CharField(max_length=120, default='Full Body')
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=40, default='Beginner')
    days_per_week = models.PositiveIntegerField(default=3)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class WorkoutPlanItem(models.Model):
    plan = models.ForeignKey(WorkoutPlan, related_name='items', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    day_label = models.CharField(max_length=50, default='Day 1')
    sets = models.PositiveIntegerField(default=3)
    reps = models.CharField(max_length=50, default='8-12')
    rest_seconds = models.PositiveIntegerField(default=60)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']


class WorkoutSession(models.Model):
    user = models.ForeignKey(User, related_name='workout_sessions', on_delete=models.CASCADE)
    plan = models.ForeignKey(WorkoutPlan, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=160)
    status = models.CharField(max_length=30, default='completed')
    duration_minutes = models.PositiveIntegerField(default=45)
    perceived_exertion = models.PositiveIntegerField(default=6)
    calories_estimate = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)


class ProgressEntry(models.Model):
    METRIC_CHOICES = [
        ('weight', 'Body weight'), ('body_fat', 'Body fat'), ('waist', 'Waist'), ('chest', 'Chest'),
        ('hip', 'Hip'), ('arm', 'Arm'), ('thigh', 'Thigh'), ('resting_hr', 'Resting heart rate'),
        ('sleep', 'Sleep hours'), ('water', 'Water intake'), ('steps', 'Steps'), ('calories', 'Calories'),
        ('protein', 'Protein'), ('readiness', 'Readiness score'), ('workout_volume', 'Workout volume'),
    ]
    user = models.ForeignKey(User, related_name='progress_entries', on_delete=models.CASCADE)
    metric = models.CharField(max_length=80, choices=METRIC_CHOICES)
    value = models.FloatField()
    unit = models.CharField(max_length=20, default='')
    recorded_at = models.DateField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['recorded_at']

    def __str__(self):
        return f'{self.user} - {self.metric}'


class Recommendation(models.Model):
    user = models.ForeignKey(User, related_name='recommendations', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=160)
    body = models.TextField()
    category = models.CharField(max_length=40, default='training')
    priority = models.CharField(max_length=20, default='medium')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FormSubmission(models.Model):
    exercise = models.ForeignKey(Exercise, related_name='form_submissions', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, related_name='form_submissions', on_delete=models.SET_NULL, null=True, blank=True)
    user_name = models.CharField(max_length=120, default='Guest User')
    uploaded_file = models.FileField(upload_to='user_form_uploads/')
    reference_media = models.ForeignKey(ReferenceMedia, null=True, blank=True, on_delete=models.SET_NULL)
    score = models.FloatField(default=0)
    status = models.CharField(max_length=30, default='processed')
    feedback = models.JSONField(default=list, blank=True)
    analysis_summary = models.TextField(blank=True)
    detected_landmarks = models.JSONField(default=dict, blank=True)
    reference_landmarks = models.JSONField(default=dict, blank=True)
    angle_results = models.JSONField(default=list, blank=True)
    overlay_coordinates = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_name} - {self.exercise}'


class SiteContent(models.Model):
    key = models.CharField(max_length=80, unique=True)
    value = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key
