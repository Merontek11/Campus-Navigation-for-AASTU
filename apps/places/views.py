from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Place, Event, GalleryImage, Category
from .serializers import PlaceSerializer, EventSerializer, GalleryImageSerializer, CategorySerializer
from .permissions import IsAdminUserOrReadOnly
import re
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .serializers import CategorySerializer, PlaceSerializer
from django.utils import timezone
from rest_framework.views import APIView

class PlaceListCreateView(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name'] 
    filterset_fields = ['category']  
    def perform_create(self, serializer):
        serializer.save()  
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "🎉 Place added successfully!",
            "place": response.data
        }, status=status.HTTP_201_CREATED)
    def get_queryset(self):
        queryset = Place.objects.all()
        search_query = self.request.query_params.get('search', '')

        
        if len(search_query) > 100:
            return queryset.none()  

        
        clean_query = re.sub(r'[^a-zA-Z0-9\s]', '', search_query).strip()

        if clean_query:
            queryset = queryset.filter(name__icontains=clean_query)

        return queryset

class PlaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAdminUserOrReadOnly]  
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "message": "✏️ Place updated successfully!",
            "place": response.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "message": "🗑️ Place deleted successfully!"
        }, status=status.HTTP_204_NO_CONTENT)

class PlaceSyncView(APIView):
    def get(self, request):
        places = Place.objects.all().values('id', 'name', 'category', 'latitude', 'longitude', 'description', 'image')
        return Response(list(places), status=200)

class EventListCreateView(generics.ListCreateAPIView):
      queryset = Event.objects.all().order_by('-start_date')
      serializer_class = EventSerializer
      permission_classes = [IsAdminUserOrReadOnly]
      filter_backends = [filters.SearchFilter]
      search_fields = ['title', 'description', 'category', 'location__name']

      def perform_create(self, serializer):
          serializer.save()
class OngoingEventsView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        now = timezone.now()
        return Event.objects.filter(start_date__lte=now, end_date__gte=now)

class UpcomingEventsView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        now = timezone.now()
        return Event.objects.filter(start_date__gt=now)

class CompletedEventsView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        now = timezone.now()
        return Event.objects.filter(end_date__lt=now)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
      queryset = Event.objects.all()
      serializer_class = EventSerializer
      permission_classes = [IsAdminUserOrReadOnly]

class GalleryImageListCreateView(generics.ListCreateAPIView):
      queryset = GalleryImage.objects.filter(approved=True).order_by('-created_at')
      serializer_class = GalleryImageSerializer
      permission_classes = [permissions.IsAuthenticatedOrReadOnly]

      def perform_create(self, serializer):
          serializer.save(uploaded_by=self.request.user, approved=False)

class GalleryImagePendingApprovalView(generics.ListAPIView):
      queryset = GalleryImage.objects.filter(approved=False)
      serializer_class = GalleryImageSerializer
      permission_classes = [IsAdminUserOrReadOnly]

class GalleryImageApproveView(generics.UpdateAPIView):
      queryset = GalleryImage.objects.all()
      serializer_class = GalleryImageSerializer
      permission_classes = [IsAdminUserOrReadOnly]

      def patch(self, request, *args, **kwargs):
          image = self.get_object()
          image.approved = True
          image.save()
          return Response({"message": "✅ Image approved!"})

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]