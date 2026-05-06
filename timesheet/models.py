from django.db import models
from django.contrib.auth.models import User


# -------------------------------
# Timesheet Model
# -------------------------------
class Timesheet(models.Model):

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="timesheets"
    )
    date = models.DateField()
    project = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('employee', 'date')  # 🚀 prevents duplicate timesheets per day

    def __str__(self):
        return f"{self.employee.username} - {self.date}"


# -------------------------------
# WorkLog Model
# -------------------------------
class WorkLog(models.Model):

    STATUS_CHOICES = [
        ('COMPLETED', 'Completed'),
        ('IN_PROGRESS', 'In Progress'),
        ('PENDING', 'Pending'),
    ]

    TASK_CHOICES = [
        ('Development', 'Development'),
        ('Testing', 'Testing'),
        ('Debugging', 'Debugging'),
        ('Standup', 'Daily Standup'),
    ]

    timesheet = models.ForeignKey(
        Timesheet,
        on_delete=models.CASCADE,
        related_name='work_logs'
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    # ✅ Dropdown based task
    task = models.CharField(
        max_length=50,
        choices=TASK_CHOICES
    )

    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.task} ({self.status})"


# -------------------------------
# Notes Model
# -------------------------------
class Notes(models.Model):

    timesheet = models.OneToOneField(
        Timesheet,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    blockers = models.TextField(blank=True, null=True)
    pending_work = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Notes for {self.timesheet.employee.username}"