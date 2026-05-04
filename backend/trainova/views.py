from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .form_analysis import analyze_reference_media, analyze_uploaded_form, model_status
from .models import (
    Exercise,
    ExerciseAngleStandard,
    FitnessProfile,
    FormSubmission,
    ProgressEntry,
    Recommendation,
    ReferenceMedia,
    SiteContent,
    WorkoutPlan,
    WorkoutSession,
)
from .serializers import (
    ExerciseAngleStandardSerializer,
    ExerciseSerializer,
    FitnessProfileSerializer,
    FormSubmissionSerializer,
    ProgressEntrySerializer,
    RecommendationSerializer,
    ReferenceMediaSerializer,
    RegisterSerializer,
    UserSerializer,
    WorkoutPlanSerializer,
    WorkoutSessionSerializer,
    auth_payload,
)


class HealthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            "status": "ok",
            "service": "Trainova API",
            "pose_engine": model_status(),
        })


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(auth_payload(user), status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get("email") or request.data.get("username") or "").lower().strip()
        password = request.data.get("password") or ""
        user = authenticate(username=email, password=password)
        if not user:
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(auth_payload(user))


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(auth_payload(request.user))

    def patch(self, request):
        profile, _ = FitnessProfile.objects.get_or_create(user=request.user)
        serializer = FitnessProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(auth_payload(request.user))


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if refresh:
            try:
                RefreshToken(refresh).blacklist()
            except Exception:
                pass
        return Response({"detail": "Logged out"})


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.filter(is_active=True).prefetch_related("references", "angle_standards").order_by("name")
    serializer_class = ExerciseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "body_part", "target_muscle", "equipment", "difficulty", "movement_pattern"]
    ordering_fields = ["name", "difficulty", "body_part"]

    def get_queryset(self):
        qs = super().get_queryset()
        for field in ["body_part", "equipment", "difficulty"]:
            val = self.request.query_params.get(field)
            if val:
                qs = qs.filter(**{f"{field}__iexact": val})
        return qs


class ExerciseAngleStandardViewSet(viewsets.ModelViewSet):
    queryset = ExerciseAngleStandard.objects.select_related("exercise").order_by("exercise__name", "name")
    serializer_class = ExerciseAngleStandardSerializer


class ReferenceMediaViewSet(viewsets.ModelViewSet):
    queryset = ReferenceMedia.objects.select_related("exercise").order_by("-created_at")
    serializer_class = ReferenceMediaSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        self._update_reference_landmarks(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._update_reference_landmarks(instance)

    @staticmethod
    def _update_reference_landmarks(instance):
        if instance.file:
            analysis = analyze_reference_media(instance.file.path)
            instance.landmark_data = analysis.get("landmarks", {})
            instance.overlay_data = analysis.get("overlay", [])
            instance.save(update_fields=["landmark_data", "overlay_data"])


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.prefetch_related("items__exercise").order_by("-created_at")
    serializer_class = WorkoutPlanSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = FitnessProfile.objects.select_related("user").order_by("-created_at")
    serializer_class = FitnessProfileSerializer


class ProgressEntryViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressEntrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = ProgressEntry.objects.select_related("user").order_by("recorded_at")
        if self.request.user.is_authenticated:
            return qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = WorkoutSession.objects.select_related("user", "plan").order_by("-completed_at")
        if self.request.user.is_authenticated:
            return qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.filter(is_active=True).order_by("-created_at")
    serializer_class = RecommendationSerializer


class FormSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = FormSubmissionSerializer

    def get_queryset(self):
        qs = FormSubmission.objects.select_related("exercise", "user", "reference_media").order_by("-created_at")
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            return qs.filter(user=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user if request.user.is_authenticated else None
        instance = serializer.save(
            user=user,
            user_name=(user.get_full_name() or user.email) if user else request.data.get("user_name", "Guest User"),
            status="processing",
        )

        reference = instance.reference_media or (
            instance.exercise.references.filter(is_correct_form=True).first() if instance.exercise else None
        )
        if reference and reference.file and not reference.landmark_data:
            reference_analysis = analyze_reference_media(reference.file.path)
            reference.landmark_data = reference_analysis.get("landmarks", {})
            reference.overlay_data = reference_analysis.get("overlay", [])
            reference.save(update_fields=["landmark_data", "overlay_data"])

        analysis = analyze_uploaded_form(instance.uploaded_file.path, instance.exercise, reference)
        instance.score = analysis["score"]
        instance.feedback = analysis["feedback"]
        instance.analysis_summary = analysis["summary"]
        instance.detected_landmarks = analysis["detected_landmarks"]
        instance.reference_landmarks = analysis["reference_landmarks"]
        instance.angle_results = analysis["angle_results"]
        instance.overlay_coordinates = analysis["overlay_coordinates"]
        instance.status = "processed"
        instance.save()
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)


class DashboardView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = request.user if request.user.is_authenticated else User.objects.filter(username="alex@example.com").first() or User.objects.first()
        profile = None
        if user:
            profile, _ = FitnessProfile.objects.get_or_create(user=user)

        plan = WorkoutPlan.objects.prefetch_related("items__exercise").first()
        recommendations = Recommendation.objects.filter(is_active=True)
        if user:
            recommendations = recommendations.filter(user__isnull=True) | Recommendation.objects.filter(user=user, is_active=True)
        recommendations = recommendations.distinct().order_by("-created_at")

        progress = ProgressEntry.objects.filter(user=user).order_by("recorded_at") if user else ProgressEntry.objects.all().order_by("recorded_at")
        body_parts = Exercise.objects.values("body_part").annotate(count=Count("id")).order_by("body_part")
        weekly_target = profile.weekly_target if profile else 4
        sessions = WorkoutSession.objects.filter(user=user).count() if user else WorkoutSession.objects.count()

        return Response({
            "user": UserSerializer(user).data if user else None,
            "profile": FitnessProfileSerializer(profile).data if profile else None,
            "stats": [
                {"label": "Exercise Library", "value": Exercise.objects.count(), "helper": "curated movements"},
                {"label": "Workout Sessions", "value": sessions, "helper": "logged training sessions"},
                {"label": "AI Reviews", "value": FormSubmission.objects.count(), "helper": "technique checks"},
                {"label": "Weekly Target", "value": weekly_target, "helper": "sessions per week"},
            ],
            "todayWorkout": WorkoutPlanSerializer(plan, context={"request": request}).data if plan else None,
            "recommendations": RecommendationSerializer(recommendations[:3], many=True).data,
            "progress": ProgressEntrySerializer(progress, many=True).data,
            "bodyParts": list(body_parts),
            "poseEngine": model_status(),
        })


class SiteContentView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        content = {item.key: item.value for item in SiteContent.objects.all()}
        return Response(content)
