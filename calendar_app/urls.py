'''from django.urls import path
from calendar_app.views import *
 
urlpatterns = [
 
    path('calendar/',calendar_home),
]'''
from django.urls import path
from .views import calendar_home, attendance_events

urlpatterns = [

    path("calendar/", calendar_home, name="calendar_home"),

    path("attendance-events/", attendance_events, name="attendance_events"),

]