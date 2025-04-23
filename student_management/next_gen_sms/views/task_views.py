from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from next_gen_sms.models import DailyTask


@login_required
def manage_tasks(request):
    tasks = DailyTask.objects.all()
    return render(request, 'tasks/manage_tasks.html', {'tasks': tasks})

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(DailyTask, id=task_id)
    task.completed = not task.completed
    task.save()
    messages.success(request, 'Task status updated successfully.')
    return redirect('next_gen_sms:manage_tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(DailyTask, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('next_gen_sms:manage_tasks')
    return render(request, 'tasks/delete_task.html', {'task': task})