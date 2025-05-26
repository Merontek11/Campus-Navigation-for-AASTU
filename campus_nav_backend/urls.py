from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Campus Navigation API!")


urlpatterns = [
      path('', home),
      path('admin/', admin.site.urls),
      path('api/', include('apps.core.urls')),
      path('api/', include('apps.places.urls')),
      path('api/', include('apps.navigation.urls')),
      path('api/', include('apps.feedback.urls')),
      
  ]

if settings.DEBUG:
      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)