from django.urls import path
from .views import attendance_details, punch_in, punch_out, attendance_calendar

urlpatterns = [
    path('', attendance_details, name='attendance'),
    path('punch-in/', punch_in, name='punch_in'),
    path('punch-out/', punch_out, name='punch_out'),
    path('calendar/', attendance_calendar, name='attendance_calendar'),
]