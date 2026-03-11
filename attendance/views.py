from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from accounts.models import Registration
from .models import Attendance
from .services.attendance_services import compute_attendance


# ---------------- Attendance Page ----------------
@login_required
def attendance_details(request):

    employee = Registration.objects.filter(email=request.user.email).first()

    if not employee:
        messages.error(request, "Registration profile not found.")
        return redirect("base")

    today = timezone.now().date()

    attendance = Attendance.objects.filter(
        employee=employee,
        date=today
    ).first()

    work_hours = "0h 0m"

    if attendance and attendance.work_duration:
        total_seconds = int(attendance.work_duration.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        work_hours = f"{hours}h {minutes}m"

    context = {
        "attendance": attendance,
        "work_hours": work_hours
    }

    return render(request, "attendance/attendance.html", context)


# ---------------- Punch In ----------------
@login_required
def punch_in(request):

    employee = Registration.objects.filter(email=request.user.email).first()

    if not employee:
        messages.error(request, "Registration profile not found.")
        return redirect(request.META.get('HTTP_REFERER'))

    today = timezone.now().date()

    attendance, created = Attendance.objects.get_or_create(
        employee=employee,
        date=today
    )

    if attendance.punch_in:
        messages.error(request, "Already punched in.")
    else:
        attendance.punch_in = timezone.now()
        attendance.status = "Present"
        attendance.save()
        messages.success(request, "Punch in successful.")

    return redirect(request.META.get('HTTP_REFERER'))


# ---------------- Punch Out ----------------
@login_required
def punch_out(request):

    employee = Registration.objects.filter(email=request.user.email).first()

    if not employee:
        messages.error(request, "Registration profile not found.")
        return redirect(request.META.get('HTTP_REFERER'))

    today = timezone.now().date()

    try:
        attendance = Attendance.objects.get(employee=employee, date=today)
    except Attendance.DoesNotExist:
        messages.error(request, "Punch in first.")
        return redirect(request.META.get('HTTP_REFERER'))

    if attendance.punch_out:
        messages.error(request, "Already punched out.")
    else:
        attendance.punch_out = timezone.now()
        attendance = compute_attendance(attendance)
        attendance.save()
        messages.success(request, "Punch out successful.")

    return redirect(request.META.get('HTTP_REFERER'))

    # ---------------- Attendance Calendar ----------------
@login_required
def attendance_calendar(request):

    employee = Registration.objects.filter(email=request.user.email).first()

    if not employee:
        messages.error(request, "Registration profile not found.")
        return redirect("attendance")

    records = Attendance.objects.filter(employee=employee).order_by('-date')

    # Format working hours
    for record in records:
        if record.work_duration:
            total_seconds = int(record.work_duration.total_seconds())

            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            record.formatted_hours = f"{hours}h {minutes}m"
        else:
            record.formatted_hours = "0h 0m"

    context = {
        "records": records
    }

    return render(request, "attendance/attendance_calendar.html", context)