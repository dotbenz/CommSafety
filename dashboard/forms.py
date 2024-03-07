from django import forms
from .models import AnonymousReport, CitizenReport, Profile
from django.contrib.auth.models import User

class AnonymousReportForm(forms.ModelForm):
    class Meta:
        model = AnonymousReport
        fields = ['crime', 'description', 'crime_location', 'image_evidence']
        widgets = {
            'crime': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a crime'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'crime_location': forms.TextInput(attrs={'class': 'form-control'}),
            'image_evidence': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }
class CitizenReportForm(forms.ModelForm):
    class Meta:
        model = CitizenReport
        fields = ['crime', 'description', 'crime_location', 'image_evidence']
        widgets = {
            'crime': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a crime'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'crime_location': forms.TextInput(attrs={'class': 'form-control'}),
            'image_evidence': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }


class CitizenReportStatusForm(forms.ModelForm):
    class Meta:
        model = CitizenReport
        fields = ['status']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'image']
