from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from next_gen_sms.models import Attendance
from next_gen_sms.forms import AttendanceForm

@login_required
def attendance_overview(request):
    attendance_records = Attendance.objects.all()
    return render(request, 'attendance/attendance_overview.html', {'attendance_records': attendance_records})

@login_required
@user_passes_test(lambda u: u.is_teacher() or u.is_admin())
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance record created successfully.')
            return redirect('next_gen_sms:attendance_overview')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/attendance_create.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_teacher() or u.is_admin())
def attendance_detail(request, pk):
    attendance = get_object_or_404(Attendance, id=pk)
    return render(request, 'attendance/attendance_detail.html', {'attendance': attendance})

@login_required
@user_passes_test(lambda u: u.is_teacher() or u.is_admin())
def attendance_edit(request, pk):
    attendance = get_object_or_404(Attendance, id=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance record updated successfully.')
            return redirect('next_gen_sms:attendance_detail', attendance_id=attendance.id)
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'attendance/attendance_edit.html', {'form': form})
