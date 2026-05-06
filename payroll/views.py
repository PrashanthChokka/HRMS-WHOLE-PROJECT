from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date

from accounts.models import Registration
from attendance.models import Leave
from .models import Payroll
from .services import calculate_salary
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


# ---------------- GENERATE PAYROLL (SINGLE EMPLOYEE) ----------------
@login_required
def generate_payroll(request):

    employee = Registration.objects.filter(email=request.user.email).first()

    today = date.today()
    month = today.month
    year = today.year

    # ✅ Dynamic salary
    basic = employee.salary

    # ✅ Leave count
    leave_days = Leave.objects.filter(
        employee=employee,
        status="Approved",
        start_date__month=month,
        start_date__year=year
    ).count()

    # ✅ Calculate salary
    salary = calculate_salary(basic, leave_days)

    # 🚨 Prevent duplicate
    if Payroll.objects.filter(employee=employee, month=month, year=year).exists():
        return redirect("payroll_list")

    # ✅ Save payroll
    Payroll.objects.create(
        employee=employee,
        month=month,
        year=year,
        basic_salary=basic,
        hra=salary["hra"],
        allowances=salary["allowances"],
        bonus=0,  # optional
        leave_deduction=salary["leave_deduction"],
        pf=salary["pf"],
        tax=salary["tax"],
        gross_salary=salary["gross"],
        net_salary=salary["net"]
    )

    return redirect("payroll_list")


# ---------------- PAYROLL LIST ----------------
@login_required
def payroll_list(request):

    employee = Registration.objects.filter(email=request.user.email).first()

    payrolls = Payroll.objects.filter(employee=employee).order_by("-year", "-month")

    return render(request, "payroll/payroll_list.html", {
        "payrolls": payrolls
    })


# ---------------- GENERATE ALL PAYROLL ----------------
@login_required
def generate_all_payroll(request):

    employees = Registration.objects.all()

    today = date.today()
    month = today.month
    year = today.year

    for employee in employees:

        if Payroll.objects.filter(employee=employee, month=month, year=year).exists():
            continue

        # ✅ Dynamic salary
        basic = employee.salary

        leave_days = Leave.objects.filter(
            employee=employee,
            status="Approved",
            start_date__month=month,
            start_date__year=year
        ).count()

        salary = calculate_salary(basic, leave_days)

        Payroll.objects.create(
            employee=employee,
            month=month,
            year=year,
            basic_salary=basic,
            hra=salary["hra"],
            allowances=salary["allowances"],
            bonus=0,
            leave_deduction=salary["leave_deduction"],
            pf=salary["pf"],
            tax=salary["tax"],
            gross_salary=salary["gross"],
            net_salary=salary["net"]
        )

    return redirect("payroll_list")


# ---------------- VIEW PAYSLIP ----------------
@login_required
def view_payslip(request, payroll_id):

    payroll = Payroll.objects.get(id=payroll_id)

    return render(request, "payroll/payslip.html", {
        "payroll": payroll
    })


# ---------------- DOWNLOAD PAYSLIP ----------------
def download_payslip(request, payroll_id):

    payroll = Payroll.objects.get(id=payroll_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="payslip.pdf"'

    p = canvas.Canvas(response)

    # ---------------- HEADER ----------------
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(300, 800, "SILICON ACCESS")

    p.setFont("Helvetica", 12)
    p.drawCentredString(300, 780, "PAYSLIP")

    # ---------------- EMPLOYEE DETAILS ----------------
    p.drawString(50, 740, f"Employee: {payroll.employee.email}")
    p.drawString(50, 720, f"Month: {payroll.month}/{payroll.year}")

    # ---------------- TABLE ----------------
    data = [
        ["Component", "Amount"],

        # Earnings
        ["Basic Salary", payroll.basic_salary],
        ["HRA", payroll.hra],
        ["Allowances", payroll.allowances],
        ["Bonus", payroll.bonus],

        ["Gross Salary", payroll.gross_salary],

        # Deductions
        ["PF Deduction", payroll.pf],
        ["Tax Deduction", payroll.tax],
        ["Leave Deduction", payroll.leave_deduction],

        # Final
        ["Net Salary", payroll.net_salary],
    ]

    table = Table(data, colWidths=[250, 150])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(p, 50, 600)
    table.drawOn(p, 50, 500)

    # ---------------- FOOTER ----------------
    p.setFont("Helvetica", 10)
    p.drawString(50, 460, "This is a system-generated payslip.")

    p.save()
    return response