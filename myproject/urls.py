from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import admin_overview_view, overview_view

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ Django Admin Panel
    path('myapp/', include('myapp.urls')),  # ✅ Include myapp URLs
]

