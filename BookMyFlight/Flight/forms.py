from django import forms

class CheckInForm(forms.Form): 
    ref = forms.CharField(max_length=6, label="Ticket_Reference_Number")
    