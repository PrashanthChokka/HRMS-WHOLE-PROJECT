def compute_attendance(attendance):

    if attendance.punch_in and attendance.punch_out:

        duration = attendance.punch_out - attendance.punch_in

        # 🚫 Prevent negative duration (safety)
        if duration.total_seconds() < 0:
            attendance.status = "Invalid"
            return attendance

        attendance.work_duration = duration

        total_seconds = duration.total_seconds()
        hours = total_seconds / 3600

        # ✅ FINAL LOGIC
        if hours >= 8:
            attendance.status = "Present"

        elif hours >= 4:
            attendance.status = "Half Day"

        elif hours > 0:
            attendance.status = "Absent"

        else:
            attendance.status = "Absent"

    return attendance