# Create your models here.
from django.db import models
from accounts.models import Registration

# ---------------- SHIFT MODEL ----------------
class Shift(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    grace_minutes = models.IntegerField(default=10)
    required_hours = models.IntegerField(default=8)

    def __str__(self):
        return self.name


# ---------------- ATTENDANCE MODEL ----------------
class Attendance(models.Model):
    employee = models.ForeignKey(Registration, on_delete=models.CASCADE)
    date = models.DateField()
    punch_in = models.DateTimeField(null=True, blank=True)
    punch_out = models.DateTimeField(null=True, blank=True)
    work_duration = models.DurationField(null=True, blank=True)
    status = models.CharField(max_length=20, default="Absent")
    is_late = models.BooleanField(default=False)
    overtime = models.DurationField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee} - {self.date}"


# ---------------- LEAVE MODEL ----------------
class Leave(models.Model):

    employee = models.ForeignKey(Registration, on_delete=models.CASCADE)

    LEAVE_TYPES = [
        ('CL', 'Casual Leave (CL)'),
        ('SL', 'Sick Leave (SL)'),
        ('EL', 'Earned Leave (EL)'),
        ('LOP', 'Loss of Pay (LOP)'),
        ('OH', 'Optional Holiday'),
    ]

    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)

    start_date = models.DateField()
    end_date = models.DateField()

    reason = models.TextField()

    document = models.FileField(upload_to="leave_documents/", null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending','Pending'),
            ('Approved','Approved'),
            ('Rejected','Rejected'),
            ('Cancelled','Cancelled')
        ],
        default="Pending"
    )
    manager_comment= models.TextField(null=True, blank=True)
    applied_on = models.DateTimeField(auto_now_add=True)

# ---------------- HOLIDAY MODEL ----------------
class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(unique=True)

    def __str__(self):
        return self.name

