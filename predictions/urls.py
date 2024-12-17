from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_activity, name='predict_activity'),
    path('history/', views.history, name='history'), 
    path('reset/', views.reset_database, name='reset_database'),  
]
