from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import (
    CustomUser, UserProfile, Course, DailyTask, Marks,
    Attendance, Certification, Event, CourseStudent
)

# ---- User & Profile Forms ----

class UserUpdateForm(forms.ModelForm):
    """ Form for updating user details (first name, last name, and email). """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """ Form for updating user profile details including picture, bio, and skills. """
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'skills', 'description', 'phone_number', 'department']


# ---- Course & Enrollment Forms ----

class CourseEnrollForm(forms.ModelForm):
    """ Form for enrolling in a course. """
    class Meta:
        model = CourseStudent
        fields = ['course']
        # if you wanted to add customuser here, you would have to exclude it from the form and add it in the view.

class CourseForm(forms.ModelForm):
    """ Form for creating or updating a course. """
    class Meta:
        model = Course
        fields = ['name', 'description', 'skills_required']

# ---- Task & Event Forms ----

class DailyTaskForm(forms.ModelForm):
    """ Form for managing daily tasks. """
    class Meta:
        model = DailyTask
        fields = ['task_description', 'completed']

class EventForm(forms.ModelForm):
    """ Form for creating or updating an event. """
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

# ---- Marks & Attendance Forms ----

class MarksForm(forms.ModelForm):
    """ Form for managing student marks. """
    class Meta:
        model = Marks
        fields = ['student', 'subject', 'semester', 'year', 'marks']

class AttendanceForm(forms.ModelForm):
    """ Form for managing student attendance. """
    class Meta:
        model = Attendance
        fields = ['student', 'status']

# ---- Certification Form ----

class CertificationForm(forms.ModelForm):
    """ Form for uploading certifications. """
    class Meta:
        model = Certification
        fields = ['title', 'file', 'issued_date']
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
        }

# ---- Settings & Authentication Forms ----

class SettingsForm(forms.Form):
    """ Form for user settings (dark mode toggle, email updates). """
    dark_mode = forms.BooleanField(required=False, label="Enable Dark Mode")

class CustomPasswordChangeForm(PasswordChangeForm):
    """ Custom form for password change with styled input fields. """
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )