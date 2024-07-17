from django.urls import path
from .views import (
    PersonListView, PersonCreateView, PersonUpdateView, PersonDeleteView, 
    AttendanceListView, home, scan_face
)

urlpatterns = [
    path('', home, name='home'),  # Home page view
    path('persons/', PersonListView.as_view(), name='person-list'),
    path('persons/add/', PersonCreateView.as_view(), name='person-create'),
    path('persons/<int:pk>/edit/', PersonUpdateView.as_view(), name='person-update'),
    path('persons/<int:pk>/delete/', PersonDeleteView.as_view(), name='person-delete'),
    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('scan-face/', scan_face, name='scan-face'),  # Face scanning view
]
