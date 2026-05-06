from django.contrib import admin
from .models import Timesheet, WorkLog, Notes

admin.site.register(Timesheet)
admin.site.register(WorkLog)
admin.site.register(Notes)
