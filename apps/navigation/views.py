from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions 
import requests 
from decouple import config  
from apps.places.models import Place
from django.http import FileResponse, JsonResponse
import os
import hashlib


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


class NavigationView(APIView):
    def post(self, request):
        try:
            start_lat = request.data.get('start_lat')
            start_lon = request.data.get('start_lon')
            end_place_id = request.data.get('end_place_id')
            vehicle = request.data.get('vehicle', 'foot')  

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
                'profile': vehicle,
                'locale': 'en',
                'instructions': 'true',
                'calc_points': 'true',
                'points_encoded': 'false'
            }

            response = requests.get(graphhopper_url, params=params)
            data = response.json()

            if 'paths' not in data or not data['paths']:
                return Response({'error': 'No route found.'}, status=status.HTTP_404_NOT_FOUND)

            path = data['paths'][0]
            readable_data = {
                "distance_km": round(path['distance'] / 1000, 2),
                "time_minutes": round(path['time'] / 60000),
                "points": path['points']['coordinates'],
                "instructions": path.get('instructions', []),
                "vehicle": vehicle
            }
            return Response(readable_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GraphDataView(APIView):
    def get(self, request):
        graph_path = r"C:\Users\hp\graphhopper\graph-cache.ghz"  # Compressed graph
        if not os.path.exists(graph_path):
            return JsonResponse({"error": "Graph data not found."}, status=404)
        
        # Calculate MD5 hash
        with open(graph_path, 'rb') as f:
            md5_hash = hashlib.md5(f.read()).hexdigest()
        
        response = FileResponse(
            open(graph_path, 'rb'),
            as_attachment=True,
            filename='graph-cache.ghz'
        )
        response['X-Graph-MD5'] = md5_hash
        return response