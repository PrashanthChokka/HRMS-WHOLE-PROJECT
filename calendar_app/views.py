from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from accounts.models import Registration
from attendance.models import Attendance
from datetime import date, timedelta
import calendar

@login_required
def calendar_home(request):
    return render(request, "calendar_app/calendar_app.html")

from datetime import date
import calendar

@login_required
def attendance_events(request):

    employee = Registration.objects.filter(email=request.user.email).first()

    today = date.today()

    year = today.year
    month = today.month

    num_days = calendar.monthrange(year, month)[1]

    events = []

    for day in range(1, num_days + 1):

        current_date = date(year, month, day)

        # ✅ SKIP WEEKENDS
        if current_date.weekday() in [5, 6]:  # 5 = Saturday, 6 = Sunday
            events.append({
                "title": "Weekend",
                "start": str(current_date),
                "color": "#9ca3af"   # gray color
            })
            continue

        record = Attendance.objects.filter(
            employee=employee,
            date=current_date
        ).first()

        title = ""

        if record:

            if record.punch_in:
                title += "In: " + record.punch_in.strftime("%H:%M")

            if record.punch_out:
                title += "\nOut: " + record.punch_out.strftime("%H:%M")

            if record.work_duration:
                seconds = int(record.work_duration.total_seconds())
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60

                title += f"\n{hours}h {minutes}m"

        else:
            if current_date < today:
                title = "Absent"

        if title:
            events.append({
                "title": title,
                "start": str(current_date),
                "color": "#ef4444" if title == "Absent" else "#3b82f6"
            })

    return JsonResponse(events, safe=False)