from django.urls import path
from .views import attendance_details, punch_in, punch_out, attendance_calendar, apply_leave, leave_history, leave_requests, approve_leave, reject_leave,cancel_leave

urlpatterns = [
    path('', attendance_details, name='attendance'),
    path('punch-in/', punch_in, name='punch_in'),
    path('punch-out/', punch_out, name='punch_out'),
    path('calendar/', attendance_calendar, name='attendance_calendar'),

    path("apply-leave/", apply_leave, name="apply_leave"),
    path("leave-history/", leave_history, name="leave_history"),

    path("leave-requests/", leave_requests, name="leave_requests"),
    path("approve-leave/<int:leave_id>/", approve_leave, name="approve_leave"),
    path("reject-leave/<int:leave_id>/", reject_leave, name="reject_leave"),
    path("cancel-leave/<int:leave_id>/", cancel_leave, name="cancel_leave"),
]