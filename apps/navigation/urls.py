from django.urls import path
from .views import RouteView, NavigationView, GraphDataView

urlpatterns = [
      path('route/', RouteView.as_view(), name='route'),
      path('navigation/', NavigationView.as_view(), name='navigation'),
      path('graph-data/', GraphDataView.as_view(), name='graph_data'),
  ]