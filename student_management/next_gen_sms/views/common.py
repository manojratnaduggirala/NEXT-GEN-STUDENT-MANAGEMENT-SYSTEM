from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from next_gen_sms.models import Notification, CustomUser

@login_required
@user_passes_test(lambda u: u.is_admin())
def send_notification(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            admins = CustomUser.objects.filter(role='admin')
            for admin in admins:
                Notification.objects.create(user=admin, message=message, created_by=request.user)
            messages.success(request, 'Notification sent successfully.')
        else:
            messages.error(request, 'Message cannot be empty.')
        return redirect('admin_dashboard')
    return render(request, 'next_gen_sms/send_notification.html')

@login_required
def settings_view(request):
    # Placeholder settings view
    return render(request, 'next_gen_sms/settings.html')

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})
