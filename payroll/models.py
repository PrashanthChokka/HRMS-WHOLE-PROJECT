from django.db import models
from accounts.models import Registration


class Payroll(models.Model):

    employee = models.ForeignKey(Registration, on_delete=models.CASCADE)

    month = models.IntegerField()   # 1–12
    year = models.IntegerField()

    # 💰 EARNINGS
    basic_salary = models.FloatField()
    hra = models.FloatField(default=0)
    allowances = models.FloatField(default=0)
    bonus = models.FloatField(default=0)  # optional (future use)

    # ❌ DEDUCTIONS
    leave_deduction = models.FloatField(default=0)  # LOP
    pf = models.FloatField(default=0)               # Provident Fund
    tax = models.FloatField(default=0)              # TDS (Income Tax)
    other_deductions = models.FloatField(default=0)

    # 📊 SUMMARY
    gross_salary = models.FloatField()
    net_salary = models.FloatField()

    generated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')  # 🚨 prevents duplicate payroll

    def __str__(self):
        return f"{self.employee.email} - {self.month}/{self.year}"