from django.urls import path
from . import views

urlpatterns = [
    # 📋 List all timesheets
    path('', views.timesheet_list, name='timesheet_list'),

    # ➕ Create new timesheet
    path('create/', views.create_timesheet, name='create_timesheet'),

    # 🔍 View details (use clear path name)
    path('detail/<int:id>/', views.timesheet_detail, name='timesheet_detail'),
]