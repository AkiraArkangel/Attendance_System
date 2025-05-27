from django import forms
from .models import Meeting

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'date', 'time', 'venue','agenda','description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'venue': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'agenda': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2', 'rows': 4}),
            'description': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2', 'rows': 4}),
        }
