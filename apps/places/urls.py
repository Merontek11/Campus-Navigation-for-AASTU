from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
      PlaceListCreateView, PlaceDetailView,
      EventListCreateView, EventDetailView,
      GalleryImageListCreateView, GalleryImagePendingApprovalView, GalleryImageApproveView,
      CategoryListCreateView, CategoryDetailView, 
        PlaceDetailView,   PlaceDetailView,
    OngoingEventsView, UpcomingEventsView, CompletedEventsView , PlaceSyncView
  )

urlpatterns = [
    path('', PlaceListCreateView.as_view(), name='place-list'),
    path('/<int:pk>/', PlaceDetailView.as_view(), name='place-detail'),
    path('/sync/', PlaceSyncView.as_view(), name='place_sync'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('gallery/', GalleryImageListCreateView.as_view(), name='gallery-list-create'),
    path('gallery/pending/', GalleryImagePendingApprovalView.as_view(), name='gallery-pending'),
    path('gallery/<int:pk>/approve/', GalleryImageApproveView.as_view(), name='gallery-approve'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('events/', EventListCreateView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/ongoing/', OngoingEventsView.as_view(), name='ongoing-events'),
    path('events/upcoming/', UpcomingEventsView.as_view(), name='upcoming-events'),
    path('events/completed/', CompletedEventsView.as_view(), name='completed-events'),
  ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





 
    
    
