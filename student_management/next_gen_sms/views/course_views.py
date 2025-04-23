from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from next_gen_sms.models import Course, CourseStudent
from next_gen_sms.forms import CourseForm

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_teacher())
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully.')
            return redirect('next_gen_sms:manage_courses')
    else:
        form = CourseForm()
    return render(request, 'courses/add_course.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_teacher())
def manage_courses(request):
    courses = Course.objects.all()
    return render(request, 'courses/manage_courses.html', {'courses': courses})

@login_required
@user_passes_test(lambda u: u.is_student())
def student_courses(request):
    enrollments = CourseStudent.objects.filter(student=request.user)
    enrolled_course_ids = enrollments.values_list('course_id', flat=True)
    all_courses = Course.objects.all()
    return render(request, 'next_gen_sms/student_courses.html', {
        'enrollments': enrollments,
        'all_courses': all_courses,
        'enrolled_course_ids': enrolled_course_ids,
    })

@login_required
@user_passes_test(lambda u: u.is_student())
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'next_gen_sms/course_detail.html', {'course': course})

@login_required
@user_passes_test(lambda u: u.is_student())
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    CourseStudent.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f'Enrolled in {course.name} successfully.')
    return redirect('next_gen_sms:student_courses')

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_teacher())
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('next_gen_sms:manage_courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'next_gen_sms/edit_course.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_teacher())
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('next_gen_sms:manage_courses')
    return render(request, 'next_gen_sms/delete_course.html', {'course': course})
