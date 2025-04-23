from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import (
    CustomUser, UserProfile, Course, DailyTask, Marks,
    Attendance, Certification, Event, CourseStudent, Exam, ExamResult
)


from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'role')  # customize as per your model


# Role-based access decorator
def restrict_form_access(user, allowed_roles):
    """ Restricts form access based on user roles. """
    if user.role not in allowed_roles:
        raise forms.ValidationError("You do not have permission to access this form.")

# ---- User & Profile Forms ----

class UserUpdateForm(forms.ModelForm):
    """ Form for updating user details (first name, last name, and email). """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            restrict_form_access(user, ['admin', 'student', 'instructor'])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """ Form for updating user profile details including name, bio, and skills. """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            restrict_form_access(user, ['admin', 'student', 'instructor'])

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'bio', 'skills', 'description', 'phone_number', 'department']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name'
        }

class ProfileImageUpdateForm(forms.ModelForm):
    """ Form for updating user profile image. """
    class Meta:
        model = CustomUser
        fields = ['profile_image']


# ---- Course & Enrollment Forms ----

class CourseEnrollForm(forms.ModelForm):
    """ Form for enrolling in a course. """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            restrict_form_access(user, ['student'])
    
    class Meta:
        model = CourseStudent
        fields = ['course']


class CourseForm(forms.ModelForm):
    """ Form for creating or updating a course. Restricted to admin and instructors. """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            restrict_form_access(user, ['admin', 'instructor'])
    
    class Meta:
        model = Course
        fields = ['code', 'name', 'instructor', 'credits', 'schedule', 'room', 'description', 'youtube_url', 'skills_required']

# ---- Task & Event Forms ----

class DailyTaskForm(forms.ModelForm):
    """ Form for managing daily tasks. Restricted to students. """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            restrict_form_access(user, ['student'])
    
    class Meta:
        model = DailyTask
        fields = ['task_description', 'completed']


class EventForm(forms.ModelForm):
    """ Form for creating or updating an event. Restricted to admins and instructors. """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            restrict_form_access(user, ['admin', 'instructor'])
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

# ---- Marks & Attendance Forms ----

class MarksForm(forms.ModelForm):
    """ Form for managing student marks. Restricted to instructors. """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            restrict_form_access(user, ['instructor'])
            # Only show students in the student dropdown
            self.fields['student'].queryset = CustomUser.objects.filter(role='student')
    
    class Meta:
        model = Marks
        fields = ['student', 'subject', 'semester', 'year', 'marks']


class AttendanceForm(forms.ModelForm):
    """ Form for managing student attendance. Restricted to instructors. """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            restrict_form_access(self.user, ['teacher'])
            # Only show students in the student dropdown
            self.fields['student'].queryset = CustomUser.objects.filter(role='student')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.teacher = self.user
        if commit:
            instance.save()
        return instance
    
    class Meta:
        model = Attendance
        fields = ['student', 'status']
        widgets = {
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

# ---- Certification Form ----

class CertificationForm(forms.ModelForm):
    """ Form for uploading certifications. Restricted to students. """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            restrict_form_access(user, ['student'])
    
    class Meta:
        model = Certification
        fields = ['title', 'file', 'issued_date']
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
        }





# ---- Settings & Authentication Forms ----

class SettingsForm(forms.Form):
    """ Form for user settings (dark mode toggle, email updates). Accessible to all roles. """
    dark_mode = forms.BooleanField(required=False, label="Enable Dark Mode")


class CustomPasswordChangeForm(PasswordChangeForm):
    """ Custom form for password change with styled input fields. Accessible to all users. """
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

class ExamForm(forms.ModelForm):
    """ Form for managing exams. Restricted to admins and instructors. """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            restrict_form_access(user, ['admin', 'instructor'])
    
    class Meta:
        model = Exam
        fields = ['course', 'exam_type', 'date', 'start_time', 'end_time', 'location', 'max_marks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['exam', 'student', 'marks_obtained', 'grade']