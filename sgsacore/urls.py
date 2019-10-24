from django.contrib import admin
from django.urls import path, include
from .views import landing#, error_404
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name="landing"),
    path('usuario/', include('users.urls')),
    path('situaciones/', include('situacionesadms.urls')),
    # path('situ/', include('situacionesadms.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

#handler404 = error_404