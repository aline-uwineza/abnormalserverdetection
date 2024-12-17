from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('activity/', include('predictions.urls')),
    path('', RedirectView.as_view(url='/activity/predict/', permanent=True)),  # Redirect root to /activity/predict/
]
