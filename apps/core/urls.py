from django.urls import path
from .views import RegisterView, UserDetailView,  UserDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
      path('auth/register/', RegisterView.as_view(), name='register'),
      path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
      path('auth/user/', UserDetailView.as_view(), name='user_detail'),
      path('me/', UserDetailView.as_view(), name='user-detail'),
      path('register/', RegisterView.as_view(), name='register'),
      path('profile/', UserDetailView.as_view(), name='user-profile'),
      path('profile/delete/', UserDeleteView.as_view(), name='user-delete'),
  ]