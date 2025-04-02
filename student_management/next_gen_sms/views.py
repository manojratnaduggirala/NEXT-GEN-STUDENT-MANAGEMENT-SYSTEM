from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponseForbidden
from functools import wraps
from django.http import HttpResponse
from django.contrib.auth import logout

# Import models and forms
from .models import CustomUser, Course, CourseStudent, UserProfile, DailyTask, Marks, Attendance, Certification, Event
from .forms import (
    UserUpdateForm, ProfileUpdateForm, CourseForm, CourseEnrollForm,
    PasswordChangeForm, DailyTaskForm, MarksForm, AttendanceForm, CertificationForm, EventForm
)

# ========================== Role-based Access Control Decorator ========================== #
def role_required(required_role):
    """
    Decorator to restrict access based on user roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role != required_role:
                return HttpResponseForbidden("❌ Access Denied!")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# ========================== Authentication Views ========================== #
def custom_login(request):
    """
    Custom login view with role-based redirection.
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(f'{user.role}_dashboard')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')
    return render(request, 'login.html')

# ========================== Dashboard Views ========================== #
@login_required
@role_required('admin')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
@role_required('student')
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

@login_required
@role_required('teacher')
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

@login_required
def dashboard(request):
    """
    Student dashboard displaying enrolled courses, pending tasks, marks, and certifications.
    """
    context = {
        'courses': request.user.enrolled_courses.all(),
        'tasks': DailyTask.objects.filter(student=request.user, completed=False),
        'marks': Marks.objects.filter(student=request.user),
        'certifications': Certification.objects.filter(student=request.user),
    }
    return render(request, 'next_gen_sms/dashboard.html', context)

# ========================== Profile Management ========================== #
@login_required
def profile(request):
    """
    Handles displaying and updating the user's profile.
    """
    user = request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user.userprofile)
    return render(request, 'next_gen_sms/profile.html', {'user_form': user_form, 'profile_form': profile_form})


def delete_account(request):
    if request.user.is_authenticated:
        user = request.user
        user.delete()
        logout(request)
        return redirect('login')  # Redirect to login or another page
    else:
        return redirect('login') # redirect if not logged in.
    

def custom_logout(request):
    """Logs out the user and redirects to the login page with a message."""
    logout(request)  # Django's built-in logout function
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to login page


# ========================== Course Management ========================== #
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = CourseStudent.objects.filter(customuser=request.user, course=course).exists()
    return render(request, 'courses/course_detail.html', {'course': course, 'is_enrolled': is_enrolled})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user in course.students.all():
        messages.warning(request, f'You are already enrolled in {course.name}.')
    else:
        CourseStudent.objects.create(customuser=request.user, course=course)
        course.students.add(request.user)
        messages.success(request, f'You have successfully enrolled in {course.name}!')
    return redirect('dashboard')

@login_required
def add_course(request):
    """Allows teachers or admins to add a new course."""
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseForm()
    return render(request, "courses/add_course.html", {"form": form})

# ========================== Task Management ========================== #
@login_required
def toggle_task(request, task_id):
    """Toggle the completion status of a task."""
    task = get_object_or_404(DailyTask, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect("manage_tasks")

def delete_task(request, task_id):
    """Delete a task based on its ID."""
    task = get_object_or_404(DailyTask, id=task_id)
    task.delete()
    return redirect("manage_tasks")

@login_required
def manage_tasks(request):
    if request.method == "POST":
        form = DailyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.student = request.user
            task.save()
            messages.success(request, "Task added successfully!")
            return redirect('manage_tasks')
    else:
        form = DailyTaskForm()
    tasks = DailyTask.objects.filter(student=request.user)
    return render(request, 'next_gen_sms/manage_tasks.html', {'form': form, 'tasks': tasks})

# ========================== Marks and Attendance ========================== #

def marks_create(request):
    """View to create a new Marks entry."""
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marks_list')  # Redirect to marks list or another appropriate URL
    else:
        form = MarksForm()
    return render(request, 'marks/marks_form.html', {'form': form})

def marks_update(request, pk):
    """View to update an existing Marks entry."""
    mark = Marks.objects.get(pk=pk)
    if request.method == 'POST':
        form = MarksForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            return redirect('marks_list')  # Redirect to marks list or another appropriate URL
    else:
        form = MarksForm(instance=mark)
    return render(request, 'marks/marks_form.html', {'form': form})

def marks_delete(request, pk):
    """View to delete an existing Marks entry."""
    mark = Marks.objects.get(pk=pk)
    if request.method == 'POST':
        mark.delete()
        return redirect('marks_list')  # Redirect to marks list or another appropriate URL
    return render(request, 'marks/marks_confirm_delete.html', {'mark': mark})

def marks_list(request):
    """View to display a list of all Marks entries."""
    marks = Marks.objects.all()
    return render(request, 'marks/marks_list.html', {'marks': marks})

def marks_detail(request, pk):
    """View to display details of a specific Marks entry."""
    mark = Marks.objects.get(pk=pk)
    return render(request, 'marks/marks_detail.html', {'mark': mark})

@login_required
def marks_overview(request):
    marks = Marks.objects.filter(student=request.user)
    marks_data = []  # Initialize an empty list to store the processed marks

    for mark in marks:
        percentage = 0  # Default percentage is 0

        if mark.total_marks > 0:
            percentage = round((mark.marks / mark.total_marks) * 100, 2)

        marks_data.append({
            "subject": mark.subject,
            "semester": mark.semester,
            "year": mark.year,
            "marks": mark.marks,
            "total_marks": mark.total_marks,
            "percentage": percentage,
        })

    return render(request, 'next_gen_sms/marks_overview.html', {'marks': marks_data})

@login_required
def attendance_overview(request):
    attendance_records = Attendance.objects.filter(student=request.user)
    total_days = attendance_records.count()
    present_count = attendance_records.filter(status=True).count()

    if total_days > 0:
        attendance_percentage = round((present_count / total_days) * 100, 2)
    else:
        attendance_percentage = 0  # Default to 0 if total_days is 0

    return render(request, 'next_gen_sms/attendance_overview.html', {
        'attendance_records': attendance_records,
        'present_count': present_count,
        'attendance_percentage': attendance_percentage,
    })

# ========================== Event Management ========================== #
@login_required
def events_list(request):
    events = Event.objects.all().order_by('date', 'time')
    return render(request, 'next_gen_sms/events_list.html', {'events': events})

@login_required
def add_event(request):
    """Handles adding a new event."""
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect("events_list")
    else:
        form = EventForm()
    return render(request, "events/add_event.html", {"form": form})

# ========================== Settings ========================== #
@login_required
def user_settings(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        password_form = PasswordChangeForm(request.user, request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile settings updated successfully.")
            return redirect("user_settings")

        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was updated successfully.")
            return redirect("user_settings")

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        password_form = PasswordChangeForm(request.user)

    return render(request, "next_gen_sms/settings.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "password_form": password_form,
    })

# ========================== Update Profile ========================== #
@login_required
def update_profile(request):
    """Handles profile updates for the logged-in user."""
    profile = request.user.userprofile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, "profile/update_profile.html", {"form": form})

# ========================== Upload Certification ========================== #
@login_required
def upload_certification(request):
    """Handles certification upload."""
    if request.method == "POST":
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.student = request.user
            certification.save()
            return redirect("certifications")
    else:
        form = CertificationForm()
    return render(request, "certifications/upload_certification.html", {"form": form})


def certifications_view(request):
    form = CertificationForm() #create an instance of the form.
    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES) #if you are using files, add request.FILES
        if form.is_valid():
            #process form data
            form.save() #if it is a ModelForm
            #or
            #process the data from form.cleaned_data
            #...
            return redirect('some_success_url') #redirect to a success page.
    context = {'form':form}
    return render(request, 'certifications/your_certifications_template.html', context)