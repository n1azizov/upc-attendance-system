from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.instructor_sessions, name='sessions'),
    path('session/<int:session_id>/', views.mark_attendance, name='mark'),
]
