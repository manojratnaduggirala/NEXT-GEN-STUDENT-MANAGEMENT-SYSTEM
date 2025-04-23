from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.contrib import messages
from next_gen_sms.models import Exam, ExamResult
from next_gen_sms.forms import ExamForm, ExamResultForm

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_teacher())
def manage_exams(request):
    exams = Exam.objects.all()
    return render(request, 'next_gen_sms/manage_exams.html', {'exams': exams})

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_teacher())
def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam added successfully.')
            return redirect('next_gen_sms:manage_exams')
    else:
        form = ExamForm()
    return render(request, 'next_gen_sms/add_exam.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_teacher())
def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam updated successfully.')
            return redirect('next_gen_sms:manage_exams')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'next_gen_sms/edit_exam.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_teacher())
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted successfully.')
        return redirect('next_gen_sms:manage_exams')
    return render(request, 'next_gen_sms/delete_exam.html', {'exam': exam})

class ExamManagementView(View):
    @login_required
    @user_passes_test(lambda u: u.is_admin() or u.is_teacher())
    def get(self, request):
        exams = Exam.objects.all()
        return render(request, 'next_gen_sms/exam_management.html', {'exams': exams})

    @login_required
    @user_passes_test(lambda u: u.is_admin() or u.is_teacher())
    def post(self, request):
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam added successfully.')
            return redirect('next_gen_sms:exam_management')
        exams = Exam.objects.all()
        return render(request, 'next_gen_sms/exam_management.html', {'exams': exams, 'form': form})
