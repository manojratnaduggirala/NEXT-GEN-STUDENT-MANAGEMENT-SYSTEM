from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from functools import wraps
from next_gen_sms.models import CustomUser, DailyTask, Marks, Attendance, Certification, Notification
from django.contrib import messages

# Role Check Functions
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'

def is_student(user):
    return user.is_authenticated and user.role == 'student'

def rate_limit_view(request):
    """Custom view for rate limited requests"""
    from django.http import HttpResponseForbidden
    return HttpResponseForbidden(
        "Too many requests. Please try again later.",
        content_type="text/plain"
    )

def rate_limit(key, rate):
    """Decorator to implement rate limiting"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            from django.conf import settings
            if not getattr(settings, 'RATELIMIT_ENABLE', True):
                return view_func(request, *args, **kwargs)
                
            cache_key = f'ratelimit:{key}:{request.META.get("REMOTE_ADDR")}'
            count = cache.get(cache_key, 0)
            
            if count >= int(rate.split('/')[0]):
                return redirect(settings.RATELIMIT_VIEW)
                
            cache.set(cache_key, count + 1, timeout=60)  # 1 minute window
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

def student_dashboard_api(request):
    # Example data — replace with real logic
    data = {
        'attendance_percentage': 85,
        'upcoming_exams': [
            {'subject': 'Math', 'date': '2025-04-15', 'time': '10:00 AM'},
            {'subject': 'Science', 'date': '2025-04-18', 'time': '2:00 PM'}
        ]
    }
    return JsonResponse(data)

@login_required
@user_passes_test(is_admin)
def admin_dashboard_api(request):
    """API endpoint for admin dashboard data"""
    data = {
        'attendance_percentage': 92,
        'upcoming_exams': [
            {'subject': 'History', 'date': '2025-04-16', 'time': '9:00 AM'},
            {'subject': 'Physics', 'date': '2025-04-19', 'time': '11:00 AM'}
        ],
        'total_students': CustomUser.objects.filter(role='student').count(),
        'total_teachers': CustomUser.objects.filter(role='teacher').count(),
        'total_courses': CustomUser.objects.count()  # Assuming courses count is in CustomUser for now
    }
    return JsonResponse(data)

@login_required
@never_cache
@rate_limit('dashboard', '10/minute')
def dashboard(request):
    if not hasattr(request.user, 'role'):
        return render(request, 'error.html', {'message': 'User role not defined'})
    
    if request.user.is_admin():
        return redirect('next_gen_sms:admin_dashboard')
    elif request.user.is_teacher():
        return redirect('next_gen_sms:teacher_dashboard')
    elif request.user.is_student():
        return redirect('next_gen_sms:student_dashboard')
    else:
        return render(request, 'error.html', {'message': 'Unknown user role'})

@login_required
@user_passes_test(is_admin)
@never_cache
@require_http_methods(["GET"])
def admin_dashboard(request):
    students = CustomUser.objects.filter(role='student').select_related('profile')
    
    recent_activities = []
    
    recent_tasks = DailyTask.objects.select_related('student').order_by('-created_at')[:5]
    for task in recent_tasks:
        recent_activities.append({
            'type': 'task',
            'student': task.student,
            'description': f"Task: {task.task_description[:50]}",
            'status': 'Completed' if task.completed else 'Pending',
            'date': task.created_at
        })
    
    recent_marks = Marks.objects.select_related('student').order_by('-id')[:5]
    for mark in recent_marks:
        recent_activities.append({
            'type': 'mark',
            'student': mark.student,
            'description': f"Mark: {mark.subject} - {mark.marks}/{mark.total_marks}",
            'date': mark.semester
        })
    
    recent_attendance = Attendance.objects.select_related('student').order_by('-date')[:5]
    for att in recent_attendance:
        recent_activities.append({
            'type': 'attendance',
            'student': att.student,
            'description': f"Attendance: {'Present' if att.status else 'Absent'}",
            'date': att.date
        })
    
    recent_activities.sort(key=lambda x: x['date'].date() if hasattr(x['date'], 'date') else x['date'], reverse=True)
    
    recent_certs = Certification.objects.select_related('student').order_by('-issued_date')[:5]
    
    return render(request, 'next_gen_sms/admin_dashboard.html', {
        'students': students,
        'total_students': students.count(),
        'total_teachers': CustomUser.objects.filter(role='teacher').count(),
        'total_courses': CustomUser.objects.count(),  # Assuming courses count is in CustomUser for now
        'unread_notifications_count': request.user.notifications.filter(is_read=False).count(),
        'recent_activities': recent_activities[:10],
        'recent_certifications': recent_certs
    })

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    student_ids = Marks.objects.filter(student__role='student').values_list('student', flat=True).distinct()
    students = CustomUser.objects.filter(id__in=student_ids).select_related('profile')
    
    return render(request, 'next_gen_sms/teacher_dashboard.html', {
        'students': students
    })

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    return render(request, 'next_gen_sms/student_dashboard.html')

@login_required
def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)
