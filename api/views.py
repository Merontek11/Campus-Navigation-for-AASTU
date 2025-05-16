from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Place
from .models import Event
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import re
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PlaceSerializer, RegisterSerializer, UserSerializer, EventSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.permissions import BasePermission
from .models import GalleryImage
from .serializers import GalleryImageSerializer
from .permissions import IsAdminUserOrReadOnly
from rest_framework.permissions import BasePermission
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

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "✅ User registered successfully!",
            "user": response.data
        }, status=status.HTTP_201_CREATED)

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
        
class RouteView(APIView):
    def get(self, request):
        start = request.query_params.get('start')  
        end = request.query_params.get('end')      
        vehicle = request.query_params.get('vehicle', 'foot')

        if not start or not end:
            return Response({"error": "Missing 'start' or 'end' parameters."}, status=400)

        graphhopper_url = 'http://localhost:8989/route'
        params = {
            'point': [start, end],
            'profile': vehicle,  
            'locale': 'en',
            'instructions': 'true',
            'calc_points': 'true',
            'points_encoded': 'false'
        }

        try:
            response = requests.get(graphhopper_url, params=params)
            data = response.json()

            if 'paths' not in data or not data['paths']:
                return Response({'error': 'No route found.'}, status=404)

            path = data['paths'][0]

            readable_data = {
                "distance_km": round(path['distance'] / 1000, 2),  
                "time_minutes": round(path['time'] / 60000),       
                "points": path['points']['coordinates'],           
                "instructions": path.get('instructions', []),      
                "vehicle": vehicle
            }

            return Response(readable_data, status=200)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=500)


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-date')
    serializer_class = EventSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'category', 'location__name']  

    def perform_create(self, serializer):
        serializer.save()



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

from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from .permissions import IsAdminUserOrReadOnly

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

class NavigationView(APIView):
    def post(self, request):
        try:
            start_lat = request.data.get('start_lat')
            start_lon = request.data.get('start_lon')
            end_place_id = request.data.get('end_place_id')

            if not (start_lat and start_lon and end_place_id):
                return Response({'error': 'start_lat, start_lon, and end_place_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                end_place = Place.objects.get(id=end_place_id)
            except Place.DoesNotExist:
                return Response({'error': 'End place not found.'}, status=status.HTTP_404_NOT_FOUND)

            end_lat = end_place.latitude
            end_lon = end_place.longitude

            graphhopper_url = 'http://localhost:8989/route'
            params = {
                'point': [f'{start_lat},{start_lon}', f'{end_lat},{end_lon}'],
                'profile': 'vehicle',
                'locale': 'en',
                'instructions': 'true',
                'calc_points': 'true'
            }

            response = requests.get(graphhopper_url, params=params)
            data = response.json()

            if 'paths' not in data:
                return Response({'error': 'Error fetching route from GraphHopper.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(data['paths'][0], status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)