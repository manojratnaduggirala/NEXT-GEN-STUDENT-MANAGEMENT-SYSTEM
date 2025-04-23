from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from next_gen_sms.models import Marks
from next_gen_sms.forms import MarksForm

@login_required
@user_passes_test(lambda u: u.is_teacher() or u.is_admin())
def marks_create(request):
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marks record created successfully.')
            return redirect('next_gen_sms:marks_list')
    else:
        form = MarksForm()
    return render(request, 'marks/marks_create.html', {'form': form})

@login_required
def marks_list(request):
    marks_records = Marks.objects.all()
    return render(request, 'marks/marks_list.html', {'marks_records': marks_records})

@login_required
def marks_detail(request, marks_id):
    marks = get_object_or_404(Marks, id=marks_id)
    return render(request, 'marks/marks_detail.html', {'marks': marks})

@login_required
def marks_overview(request):
    marks_records = Marks.objects.all()
    return render(request, 'marks/marks_overview.html', {'marks_records': marks_records})

@login_required
@user_passes_test(lambda u: u.is_teacher() or u.is_admin())
def marks_update(request, marks_id):
    marks = get_object_or_404(Marks, id=marks_id)
    if request.method == 'POST':
        form = MarksForm(request.POST, instance=marks)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marks record updated successfully.')
            return redirect('next_gen_sms:marks_detail', marks_id=marks.id)
    else:
        form = MarksForm(instance=marks)
    return render(request, 'marks/marks_update.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_teacher() or u.is_admin())
def marks_delete(request, marks_id):
    marks = get_object_or_404(Marks, id=marks_id)
    if request.method == 'POST':
        marks.delete()
        messages.success(request, 'Marks record deleted successfully.')
        return redirect('next_gen_sms:marks_list')
    return render(request, 'marks/marks_confirm_delete.html', {'marks': marks})
