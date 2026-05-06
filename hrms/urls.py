from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from employee.views import update_employee, delete_employee

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', lambda request: redirect('/accounts/login/')),

    path('e/', include('employee.urls')),
    path('a/', include('attendance.urls')),
    path('accounts/', include('accounts.urls')),

    path('update_employee/<int:id>/', update_employee),
    path('delete_employee/<int:id>/', delete_employee),

    path('c/', include('calendar_app.urls')),

    # ✅ Payroll
    path('payroll/', include('payroll.urls')),
    path('timesheet/', include('timesheet.urls')), 
]