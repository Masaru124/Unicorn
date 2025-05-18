from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('analysis/', views.analysis, name='analysis'),
    path('export/excel/', views.export_excel, name='export_excel'),
   
    path('detailed-unicorns/', views.detailed_unicorns, name='detailed_unicorns'),
]
