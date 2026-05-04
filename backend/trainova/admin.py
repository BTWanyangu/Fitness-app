from django.contrib import admin
from .models import (
    FitnessProfile, Exercise, ExerciseAngleStandard, ReferenceMedia, WorkoutPlan, WorkoutPlanItem,
    WorkoutSession, ProgressEntry, Recommendation, FormSubmission, SiteContent
)


class WorkoutPlanItemInline(admin.TabularInline):
    model = WorkoutPlanItem
    extra = 1


class ExerciseAngleStandardInline(admin.TabularInline):
    model = ExerciseAngleStandard
    extra = 1


class ReferenceMediaInline(admin.TabularInline):
    model = ReferenceMedia
    extra = 1


@admin.register(FitnessProfile)
class FitnessProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'goal', 'training_level', 'weekly_target', 'readiness_status']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'location']
    list_filter = ['goal', 'training_level', 'activity_level', 'location']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'body_part', 'target_muscle', 'equipment', 'difficulty', 'is_active']
    list_filter = ['body_part', 'equipment', 'difficulty', 'is_active']
    search_fields = ['name', 'target_muscle', 'equipment']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ExerciseAngleStandardInline, ReferenceMediaInline]


@admin.register(ExerciseAngleStandard)
class ExerciseAngleStandardAdmin(admin.ModelAdmin):
    list_display = ['exercise', 'name', 'min_degrees', 'max_degrees', 'weight']
    list_filter = ['exercise']


@admin.register(ReferenceMedia)
class ReferenceMediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'exercise', 'media_type', 'is_correct_form', 'created_at']
    list_filter = ['media_type', 'is_correct_form', 'exercise']
    search_fields = ['title', 'exercise__name']


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'focus', 'difficulty', 'days_per_week', 'is_featured']
    list_filter = ['difficulty', 'focus', 'is_featured']
    inlines = [WorkoutPlanItemInline]


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'status', 'duration_minutes', 'perceived_exertion', 'completed_at']
    list_filter = ['status', 'completed_at']
    search_fields = ['user__email', 'title']


@admin.register(ProgressEntry)
class ProgressEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'metric', 'value', 'unit', 'recorded_at']
    list_filter = ['metric', 'recorded_at']
    search_fields = ['user__email', 'metric']


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'priority', 'is_active', 'created_at']
    list_filter = ['category', 'priority', 'is_active']


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'exercise', 'score', 'status', 'created_at']
    list_filter = ['status', 'exercise', 'created_at']
    search_fields = ['user_name', 'exercise__name']
    readonly_fields = ['score', 'feedback', 'analysis_summary', 'detected_landmarks', 'reference_landmarks', 'angle_results', 'overlay_coordinates']


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ['key', 'updated_at']
    search_fields = ['key']
