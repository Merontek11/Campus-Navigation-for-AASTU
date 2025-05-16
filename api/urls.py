from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RouteView
from api.views import (
    PlaceListCreateView,
    PlaceDetailView,
    RegisterView,
    UserDetailView,
    EventListCreateView, EventDetailView,
    GalleryImageListCreateView,
    GalleryImagePendingApprovalView,
    GalleryImageApproveView,
    CategoryListCreateView, CategoryDetailView,
    NavigationView

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('places/', PlaceListCreateView.as_view(), name='place-list'),
    path('places/<int:pk>/', PlaceDetailView.as_view(), name='place-detail'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('auth/user/', UserDetailView.as_view(), name='user_detail'),
    path('route/', RouteView.as_view(), name='route'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('gallery/', GalleryImageListCreateView.as_view(), name='gallery-list-create'),
    path('gallery/pending/', GalleryImagePendingApprovalView.as_view(), name='gallery-pending'),
    path('gallery/<int:pk>/approve/', GalleryImageApproveView.as_view(), name='gallery-approve'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('navigation/', NavigationView.as_view(), name='navigation'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
