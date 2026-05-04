from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from trainova import views

router = DefaultRouter()
router.register(r'exercises', views.ExerciseViewSet)
router.register(r'exercise-standards', views.ExerciseAngleStandardViewSet)
router.register(r'reference-media', views.ReferenceMediaViewSet)
router.register(r'workouts', views.WorkoutPlanViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'progress', views.ProgressEntryViewSet, basename='progress')
router.register(r'workout-sessions', views.WorkoutSessionViewSet, basename='workout-sessions')
router.register(r'recommendations', views.RecommendationViewSet)
router.register(r'form-submissions', views.FormSubmissionViewSet, basename='form-submissions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/register/', views.RegisterView.as_view()),
    path('api/auth/login/', views.LoginView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/auth/me/', views.MeView.as_view()),
    path('api/auth/logout/', views.LogoutView.as_view()),
    path('api/site-content/', views.SiteContentView.as_view()),
    path('api/dashboard/', views.DashboardView.as_view()),
    path('api/health/', views.HealthView.as_view()),
    path('api/pose/status/', views.HealthView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
