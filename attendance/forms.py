from django import forms
from .models import Leave

class LeaveForm(forms.ModelForm):

    class Meta:
        model = Leave
        fields = ['leave_type','start_date','end_date','reason']