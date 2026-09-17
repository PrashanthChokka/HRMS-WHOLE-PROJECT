from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from datetime import date

from accounts.models import Registration
from .models import Attendance, Leave
from .forms import LeaveForm
from .services.attendance_services import compute_attendance
from payroll.models import Payroll


# ---------------- Attendance Page ----------------
@login_required
def attendance_details(request):
    employee = Registration.objects.filter(email=request.user.email).first()

    if not employee:
        messages.error(request, "Registration profile not found.", extra_tags="attendance")
        return redirect("base")

    today = timezone.now().date()
    attendance = Attendance.objects.filter(employee=employee, date=today).first()

    work_hours = "0h 0m"

    if attendance and attendance.work_duration:
        total_seconds = int(attendance.work_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        work_hours = f"{hours}h {minutes}m"

    return render(request, "attendance/attendance.html", {
        "attendance": attendance,
        "work_hours": work_hours
    })


# ---------------- Punch In ----------------
@login_required
def punch_in(request):
    employee = Registration.objects.filter(email=request.user.email).first()

    if not employee:
        messages.error(request, "Registration profile not found.", extra_tags="attendance")
        return redirect(request.META.get('HTTP_REFERER'))

    today = timezone.now().date()

    attendance, created = Attendance.objects.get_or_create(
        employee=employee,
        date=today
    )

    if attendance.punch_in:
        messages.error(request, "Already punched in.", extra_tags="attendance")
    else:
        attendance.punch_in = timezone.now()
        attendance.status = "In Progress"
        attendance.save()
        messages.success(request, "Punch in successful.", extra_tags="attendance")

    return redirect(request.META.get('HTTP_REFERER'))


# ---------------- Punch Out ----------------
@login_required
def punch_out(request):
    employee = Registration.objects.filter(email=request.user.email).first()

    if not employee:
        messages.error(request, "Registration profile not found.", extra_tags="attendance")
        return redirect(request.META.get('HTTP_REFERER'))

    today = timezone.now().date()

    try:
        attendance = Attendance.objects.get(employee=employee, date=today)
    except Attendance.DoesNotExist:
        messages.error(request, "Punch in first.", extra_tags="attendance")
        return redirect(request.META.get('HTTP_REFERER'))

    if attendance.punch_out:
        messages.error(request, "Already punched out.", extra_tags="attendance")
    else:
        attendance.punch_out = timezone.now()
        attendance = compute_attendance(attendance)
        attendance.save()
        messages.success(request, "Punch out successful.", extra_tags="attendance")

    return redirect(request.META.get('HTTP_REFERER'))


# ---------------- Attendance Calendar ----------------
@login_required
def attendance_calendar(request):
    employee = Registration.objects.filter(email=request.user.email).first()

    if not employee:
        messages.error(request, "Registration profile not found.", extra_tags="attendance")
        return redirect("attendance")

    records = Attendance.objects.filter(employee=employee).order_by('-date')

    for record in records:
        if record.work_duration:
            total_seconds = int(record.work_duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            record.formatted_hours = f"{hours}h {minutes}m"
        else:
            record.formatted_hours = "0h 0m"

    return render(request, "attendance/attendance_calendar.html", {
        "records": records
    })


# ---------------- Apply Leave ----------------
@login_required
def apply_leave(request):
    employee = Registration.objects.filter(email=request.user.username).first()

    if not employee:
        messages.error(request, "Employee not found", extra_tags="leave")
        return redirect("base")

    today = date.today()
    earned_leaves = today.month

    used_leaves = Leave.objects.filter(
        employee=employee,
        start_date__year=today.year,
        status="Approved"
    ).count()

    leave_balance = max(0, earned_leaves - used_leaves)

    form = LeaveForm()

    if request.method == "POST":
        form = LeaveForm(request.POST, request.FILES)

        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee

            if leave.end_date < leave.start_date:
                messages.error(
                    request,
                    "End date cannot be before start date",
                    extra_tags="leave"
                )
                return redirect("apply_leave")

            leave.save()

            messages.success(
                request,
                "Leave applied successfully",
                extra_tags="leave"
            )

            return redirect("leave_history")

    return render(request, "attendance/apply_leave.html", {
        "form": form,
        "leave_balance": leave_balance
    })


# ---------------- Leave History ----------------
@login_required
def leave_history(request):
    employee = Registration.objects.filter(email=request.user.email).first()

    leaves = Leave.objects.filter(employee=employee).order_by("-applied_on")

    for leave in leaves:
        leave.days = (leave.end_date - leave.start_date).days + 1

    return render(request, "attendance/leave_history.html", {
        "leaves": leaves
    })

  
# ---------------- Manager Leave Requests ----------------
@login_required
def leave_requests(request):
    if not request.user.is_staff:
        messages.error(request, "Not authorized", extra_tags="leave")
        return render(request, "attendance/access_denied.html")

    leaves = Leave.objects.filter(status="Pending").order_by("-applied_on")

    for leave in leaves:
        leave.days = (leave.end_date - leave.start_date).days + 1

    return render(request, "attendance/leave_requests.html", {
        "leaves": leaves
    })


# ---------------- Approve Leave ----------------
@login_required
def approve_leave(request, leave_id):
    leave = Leave.objects.get(id=leave_id)

    leave.status = "Approved"
    leave.save()

    messages.success(request, "Leave approved", extra_tags="leave")

    return redirect("leave_requests")


# ---------------- Reject Leave ----------------
@require_POST
@login_required
def reject_leave(request, leave_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Not allowed")

    leave = Leave.objects.get(id=leave_id)

    comment = request.POST.get("comment")

    leave.status = "Rejected"
    leave.manager_comment = comment
    leave.save()

    messages.success(request, "Leave rejected with comment", extra_tags="leave")

    return redirect("leave_requests")


# ---------------- Cancel Leave ----------------
@login_required
def cancel_leave(request, leave_id):
    leave = Leave.objects.get(id=leave_id)

    leave.status = "Cancelled"
    leave.save()

    messages.success(request, "Leave cancelled", extra_tags="leave")

    return redirect("leave_history")