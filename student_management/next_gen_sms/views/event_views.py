from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from next_gen_sms.models import Event
from next_gen_sms.forms import EventForm

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_teacher())
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added successfully.')
            return redirect('next_gen_sms:events_list')
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})

@login_required
def events_list(request):
    events = Event.objects.all()
    return render(request, 'events/events_list.html', {'events': events})

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_teacher())
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('next_gen_sms:events_list')
    return render(request, 'events/confirm_delete.html', {'event': event})

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_teacher())
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('next_gen_sms:events_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form})
