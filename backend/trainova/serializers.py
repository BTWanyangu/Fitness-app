from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    FitnessProfile, Exercise, ExerciseAngleStandard, ReferenceMedia, WorkoutPlan, WorkoutPlanItem,
    WorkoutSession, ProgressEntry, Recommendation, FormSubmission, SiteContent
)


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    phone = serializers.CharField(max_length=30, required=False, allow_blank=True)
    location = serializers.CharField(max_length=80, required=False, default='Nairobi')
    age = serializers.IntegerField(required=False, default=28)
    gender = serializers.CharField(required=False, allow_blank=True)
    height_cm = serializers.FloatField(required=False, default=170)
    weight_kg = serializers.FloatField(required=False, default=70)
    goal = serializers.CharField(required=False, default='general_fitness')
    training_level = serializers.CharField(required=False, default='beginner')
    weekly_target = serializers.IntegerField(required=False, default=4)

    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email=value).exists() or User.objects.filter(username=value).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return value

    def create(self, validated_data):
        full_name = validated_data.pop('full_name').strip()
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        first_name, _, last_name = full_name.partition(' ')
        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        FitnessProfile.objects.create(user=user, **validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'full_name']
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.email


class FitnessProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = FitnessProfile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class AuthResponseSerializer(serializers.Serializer):
    user = UserSerializer()
    profile = FitnessProfileSerializer()
    access = serializers.CharField()
    refresh = serializers.CharField()


def auth_payload(user: User):
    refresh = RefreshToken.for_user(user)
    profile, _ = FitnessProfile.objects.get_or_create(user=user)
    return {
        'user': UserSerializer(user).data,
        'profile': FitnessProfileSerializer(profile).data,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


class ExerciseAngleStandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseAngleStandard
        fields = '__all__'


class ReferenceMediaSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    class Meta:
        model = ReferenceMedia
        fields = '__all__'
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.external_url


class ExerciseSerializer(serializers.ModelSerializer):
    references = ReferenceMediaSerializer(many=True, read_only=True)
    angle_standards = ExerciseAngleStandardSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Exercise
        fields = '__all__'
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.external_image_url


class WorkoutPlanItemSerializer(serializers.ModelSerializer):
    exercise_detail = ExerciseSerializer(source='exercise', read_only=True)
    class Meta:
        model = WorkoutPlanItem
        fields = '__all__'


class WorkoutPlanSerializer(serializers.ModelSerializer):
    items = WorkoutPlanItemSerializer(many=True, read_only=True)
    class Meta:
        model = WorkoutPlan
        fields = '__all__'


class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = '__all__'
        read_only_fields = ['user', 'completed_at']


class ProgressEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressEntry
        fields = '__all__'
        read_only_fields = ['user']


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'
        read_only_fields = ['user']


class FormSubmissionSerializer(serializers.ModelSerializer):
    uploaded_url = serializers.SerializerMethodField()
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)
    class Meta:
        model = FormSubmission
        fields = '__all__'
        read_only_fields = [
            'user', 'score', 'feedback', 'analysis_summary', 'status', 'detected_landmarks',
            'reference_landmarks', 'angle_results', 'overlay_coordinates'
        ]
    def get_uploaded_url(self, obj):
        request = self.context.get('request')
        if obj.uploaded_file and request:
            return request.build_absolute_uri(obj.uploaded_file.url)
        return ''


class SiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContent
        fields = '__all__'
