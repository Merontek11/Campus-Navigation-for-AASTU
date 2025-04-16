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

class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Safe methods = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only admins can write
        return request.user and request.user.is_staff


class PlaceListCreateView(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']  # 🔍 Allows searching by name
    filterset_fields = ['category']  # 🏷️ Allows filtering by category
    def perform_create(self, serializer):
        serializer.save()  # Optional: you can add owner=self.request.user if needed
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "🎉 Place added successfully!",
            "place": response.data
        }, status=status.HTTP_201_CREATED)
    def get_queryset(self):
        queryset = Place.objects.all()
        search_query = self.request.query_params.get('search', '')

        # ✅ Basic validation: length limit
        if len(search_query) > 100:
            return queryset.none()  # too long = no match

        # ✅ Sanitization: remove special characters
        clean_query = re.sub(r'[^a-zA-Z0-9\s]', '', search_query).strip()

        if clean_query:
            queryset = queryset.filter(name__icontains=clean_query)

        return queryset

class PlaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # View: everyone | Edit/Delete: logged in only
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
    permission_classes = [permissions.AllowAny]  # Allow registration for all
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
            'vehicle': 'vehicle',  
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
                "distance_km": round(path['distance'] / 1000, 2),  # meters to km
                "time_minutes": round(path['time'] / 60000),       # ms to minutes
                "points": path['points']['coordinates'],           # for drawing map
                "instructions": path.get('instructions', []),      # turn-by-turn directions
                "vehicle": vehicle
            }

            return Response(readable_data, status=200)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=500)
        

# 📆 List and Create Events
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-date')
    serializer_class = EventSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'category', 'location__name']  # 🔍

    def perform_create(self, serializer):
        serializer.save()


# ✏️ Retrieve, Update, Delete an Event (admin only for edit/delete)
class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUserOrReadOnly]