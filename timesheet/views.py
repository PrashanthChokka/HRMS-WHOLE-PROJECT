from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import Timesheet, WorkLog, Notes


# -------------------------------
# CREATE TIMESHEET
# -------------------------------
@login_required
def create_timesheet(request):
    if request.method == "POST":

        # ❌ REMOVED employee_name
        # ✅ USING LOGGED-IN USER
        employee = request.user

        date = request.POST.get("date")
        project = request.POST.get("project")

        blockers = request.POST.get("blockers")
        pending_work = request.POST.get("pending_work")

        start_times = request.POST.getlist("start_time[]")
        end_times = request.POST.getlist("end_time[]")
        tasks = request.POST.getlist("task[]")
        descriptions = request.POST.getlist("description[]")
        statuses = request.POST.getlist("status[]")
        remarks = request.POST.getlist("remarks[]")

        has_error = False

        # -------------------------------
        # 🔒 VALIDATION
        # -------------------------------
        for i in range(len(start_times)):
            if not start_times[i] or not end_times[i] or not tasks[i]:
                continue

            try:
                start = datetime.strptime(start_times[i], "%H:%M")
                end = datetime.strptime(end_times[i], "%H:%M")
            except:
                messages.error(
                    request,
                    f"Row {i+1}: Invalid time format",
                    extra_tags="timesheet"
                )
                has_error = True
                continue

            if end <= start:
                messages.error(
                    request,
                    f"Row {i+1}: End time must be after start time",
                    extra_tags="timesheet"
                )
                has_error = True

        if has_error:
            return redirect("create_timesheet")

        # -------------------------------
        # ✅ CREATE TIMESHEET
        # -------------------------------
        timesheet = Timesheet.objects.create(
            employee=employee,   # ✅ IMPORTANT CHANGE
            date=date,
            project=project
        )

        # -------------------------------
        # ✅ CREATE WORK LOGS
        # -------------------------------
        for i in range(len(start_times)):
            if not start_times[i] or not end_times[i] or not tasks[i]:
                continue

            WorkLog.objects.create(
                timesheet=timesheet,
                start_time=start_times[i],
                end_time=end_times[i],
                task=tasks[i],
                description=descriptions[i],
                status=statuses[i],
                remarks=remarks[i]
            )

        # -------------------------------
        # ✅ CREATE NOTES
        # -------------------------------
        Notes.objects.create(
            timesheet=timesheet,
            blockers=blockers,
            pending_work=pending_work
        )

        # -------------------------------
        # ✅ SUCCESS MESSAGE
        # -------------------------------
        messages.success(
            request,
            "Timesheet saved successfully!",
            extra_tags="timesheet"
        )

        return redirect("timesheet_list")

    return render(request, "timesheet/create.html")


# -------------------------------
# LIST TIMESHEETS
# -------------------------------
@login_required
def timesheet_list(request):

    # ✅ SHOW ONLY LOGGED-IN USER DATA
    timesheets = Timesheet.objects.filter(
        employee=request.user
    ).order_by('-date')

    return render(request, "timesheet/list.html", {
        "timesheets": timesheets
    })


# -------------------------------
# TIMESHEET DETAIL
# -------------------------------
@login_required
def timesheet_detail(request, id):

    # ✅ SECURE ACCESS (only own data)
    timesheet = get_object_or_404(
        Timesheet,
        id=id,
        employee=request.user
    )

    work_logs = timesheet.work_logs.all()
    notes = getattr(timesheet, 'notes', None)

    completed_count = work_logs.filter(status="COMPLETED").count()

    return render(request, "timesheet/detail.html", {
        "timesheet": timesheet,
        "work_logs": work_logs,
        "notes": notes,
        "completed_count": completed_count
    })