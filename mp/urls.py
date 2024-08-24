# mp/urls.py

from django.contrib import admin
from django.urls import path, include
from app.views import landing_page  # Import the landing page view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landingpage'),  # Set the landing page as the root URL
    path('app/', include('app.urls')),  # Include app URLs for other views
]
