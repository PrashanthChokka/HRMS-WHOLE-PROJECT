from datetime import timedelta

def compute_attendance(attendance):
    if attendance.punch_in and attendance.punch_out:

        duration = attendance.punch_out - attendance.punch_in
        attendance.work_duration = duration

        hours = duration.total_seconds() / 3600

        if hours >= 8:
            attendance.status = "Present"

        elif hours > 0:
            attendance.status = "Half Day"

        else:
            attendance.status = "Absent"

    return attendance