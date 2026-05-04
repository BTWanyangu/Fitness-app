from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from trainova.models import (
    FitnessProfile, Exercise, ExerciseAngleStandard, WorkoutPlan, WorkoutPlanItem,
    ProgressEntry, Recommendation, SiteContent, ReferenceMedia, WorkoutSession
)

EXERCISES = [
    ('Push Up','Chest','Pectorals','Bodyweight','Beginner','push'),
    ('Barbell Bench Press','Chest','Pectorals','Barbell','Intermediate','push'),
    ('Dumbbell Press','Chest','Pectorals','Dumbbell','Beginner','push'),
    ('Squat','Legs','Quadriceps','Barbell','Intermediate','squat'),
    ('Goblet Squat','Legs','Quadriceps','Dumbbell','Beginner','squat'),
    ('Romanian Deadlift','Legs','Hamstrings','Barbell','Intermediate','hinge'),
    ('Deadlift','Back','Posterior Chain','Barbell','Advanced','hinge'),
    ('Lat Pulldown','Back','Lats','Machine','Beginner','pull'),
    ('Seated Row','Back','Mid Back','Cable','Beginner','pull'),
    ('Plank','Core','Abs','Bodyweight','Beginner','core'),
    ('Mountain Climbers','Core','Abs','Bodyweight','Beginner','conditioning'),
    ('Shoulder Press','Shoulders','Deltoids','Dumbbell','Intermediate','push'),
    ('Lateral Raise','Shoulders','Side Delts','Dumbbell','Beginner','accessory'),
    ('Biceps Curl','Arms','Biceps','Dumbbell','Beginner','pull'),
    ('Triceps Pushdown','Arms','Triceps','Cable','Beginner','push'),
    ('Lunge','Legs','Glutes','Bodyweight','Beginner','single-leg'),
    ('Hip Thrust','Glutes','Glutes','Barbell','Intermediate','hinge'),
    ('Burpee','Full Body','Conditioning','Bodyweight','Intermediate','conditioning'),
    ('Jump Rope','Cardio','Cardio','Rope','Beginner','cardio'),
    ('Kettlebell Swing','Full Body','Posterior Chain','Kettlebell','Intermediate','hinge'),
]

ANGLE_PRESETS = {
    'squat': [('Knee depth', 'left_hip', 'left_knee', 'left_ankle', 70, 115, 'Sink slightly deeper while keeping control.', 'Avoid excessive knee collapse or over-flexion.')],
    'hinge': [('Hip hinge', 'left_shoulder', 'left_hip', 'left_knee', 75, 130, 'Hinge more at the hips while keeping your back neutral.', 'You may be too upright; push hips back.')],
    'push': [('Elbow control', 'left_shoulder', 'left_elbow', 'left_wrist', 65, 160, 'Lower with control until elbows bend enough.', 'Do not lock out aggressively at the top.')],
}

class Command(BaseCommand):
    help = 'Seeds Trainova production-style starter content.'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@trainova.local', 'admin12345')

        user, _ = User.objects.get_or_create(username='alex@example.com', defaults={
            'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Mwangi'
        })
        user.set_password('password12345')
        user.save()
        profile, _ = FitnessProfile.objects.get_or_create(user=user, defaults={
            'phone': '+254700000000', 'location': 'Nairobi', 'age': 28, 'gender': 'Male',
            'height_cm': 178, 'weight_kg': 75, 'target_weight_kg': 80, 'goal': 'strength',
            'training_level': 'intermediate', 'weekly_target': 4, 'streak_days': 7,
            'available_equipment': 'Bodyweight, Dumbbells, Barbell, Cable, Machine',
            'medical_clearance_confirmed': True,
        })

        exercises = []
        for name, body, target, equip, diff, pattern in EXERCISES:
            ex, _ = Exercise.objects.get_or_create(slug=slugify(name), defaults={
                'name': name, 'body_part': body, 'target_muscle': target,
                'secondary_muscles': '', 'equipment': equip, 'difficulty': diff,
                'movement_pattern': pattern, 'description': f'{name} for {target.lower()} development.',
                'instructions': 'Warm up first, control the movement, keep a neutral spine, breathe steadily, and stop if you feel sharp pain.',
                'safety_tips': 'Use a load that allows clean technique. Prioritize range of motion and joint alignment.',
                'external_image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?q=80&w=1200&auto=format&fit=crop',
            })
            exercises.append(ex)
            ReferenceMedia.objects.get_or_create(
                exercise=ex, title=f'Correct {name} reference', defaults={
                    'media_type': 'image', 'external_url': ex.external_image_url,
                    'coaching_notes': 'Approved reference for comparison and coaching.',
                    'is_correct_form': True,
                }
            )
            for angle in ANGLE_PRESETS.get(pattern, []):
                ExerciseAngleStandard.objects.get_or_create(
                    exercise=ex, name=angle[0], defaults={
                        'joint_a': angle[1], 'joint_b': angle[2], 'joint_c': angle[3],
                        'min_degrees': angle[4], 'max_degrees': angle[5],
                        'feedback_when_low': angle[6], 'feedback_when_high': angle[7], 'weight': 1.0,
                    }
                )

        plan, _ = WorkoutPlan.objects.get_or_create(title='Nairobi Strength Foundation', defaults={
            'focus': 'Strength + Conditioning',
            'description': 'A free beginner-to-intermediate plan for gym and home users.',
            'difficulty': 'Beginner', 'days_per_week': 4,
        })
        if plan.items.count() == 0:
            for i, ex in enumerate(exercises[:8], 1):
                WorkoutPlanItem.objects.create(plan=plan, exercise=ex, day_label=f'Day {((i-1)//2)+1}', sets=4 if i < 5 else 3, reps='8-12', rest_seconds=75, order=i)

        Recommendation.objects.get_or_create(title='Prioritize clean technique', defaults={
            'body': 'Use form analysis to compare your movement against approved reference images and videos before adding more weight.',
            'priority': 'high', 'category': 'technique'
        })
        Recommendation.objects.get_or_create(title='Train consistently before increasing volume', defaults={
            'body': 'Aim for 3-4 weekly sessions and keep recovery steady before making the plan harder.',
            'priority': 'medium', 'category': 'training'
        })

        base = date.today() - timedelta(days=8)
        metrics = [
            ('weight', [75, 74.8, 74.5, 74.2, 74.0, 73.8], 'kg'),
            ('sleep', [6.2, 7.1, 6.8, 7.5, 7.0, 7.3], 'hrs'),
            ('readiness', [72, 78, 76, 83, 80, 85], '%'),
            ('steps', [6300, 7400, 8900, 9200, 8100, 10000], 'steps'),
        ]
        for metric, values, unit in metrics:
            for idx, value in enumerate(values):
                ProgressEntry.objects.get_or_create(user=user, metric=metric, recorded_at=base+timedelta(days=idx), defaults={'value': value, 'unit': unit})
        for title in ['Push Day - Upper Body', 'Lower Body Foundation', 'Full Body Conditioning']:
            WorkoutSession.objects.get_or_create(user=user, title=title, defaults={'plan': plan, 'duration_minutes': 45, 'perceived_exertion': 7, 'calories_estimate': 360})

        SiteContent.objects.get_or_create(key='landing', defaults={'value': {'heroTitle':'Train Smarter. Recover Better.','primaryCta':'Explore Our Services','secondaryCta':'More About Us'}})
        self.stdout.write(self.style.SUCCESS('Trainova starter data ready. Admin: admin / admin12345, Demo user: alex@example.com / password12345'))
