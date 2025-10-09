from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Use your working app URLs instead of MyLogin
    path('', include('IMProject.Myapp.urls')),  # points to the Myapp inside IMProject
]
