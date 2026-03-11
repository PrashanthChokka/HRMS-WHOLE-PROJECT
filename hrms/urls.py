from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
from employee import views
from employee.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', lambda request: redirect('/accounts/login/')),

    path('e/',include('employee.urls')),
    path('a/',include('attendance.urls')),
    path('accounts/', include('accounts.urls')),

    path('update_employee/<int:id>/', update_employee),
    path('delete_employee/<int:id>/', delete_employee),
]