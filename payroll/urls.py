from django.urls import path
from . import views

urlpatterns = [

    # Payroll Dashboard / List
    path("", views.payroll_list, name="payroll_list"),

    #  Generate Payroll (Logged-in Employee)
    path("generate/", views.generate_payroll, name="generate_payroll"),

    #  Generate Payroll for All Employees (Admin/Manager)
    path("generate-all/", views.generate_all_payroll, name="generate_all_payroll"),

    #  View Payslip (HTML)
    path("payslip/<int:payroll_id>/", views.view_payslip, name="view_payslip"),

    #  Download Payslip (PDF)
    path("download/<int:payroll_id>/", views.download_payslip, name="download_payslip"),
]