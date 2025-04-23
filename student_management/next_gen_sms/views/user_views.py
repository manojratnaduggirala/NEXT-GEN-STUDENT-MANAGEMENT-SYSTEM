from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import logout
from next_gen_sms.models import CustomUser
from next_gen_sms.forms import CustomUserCreationForm, ProfileUpdateForm
from next_gen_sms.forms import ProfileUpdateForm as ProfileForm

from next_gen_sms.forms import CustomUserCreationForm

@login_required
@user_passes_test(lambda u: u.is_admin())
def manage_users(request):
    search_query = request.GET.get('search', '')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            # Redirect with search query if present to maintain filtering
            if search_query:
                return redirect(f"{request.path}?search={search_query}")
            else:
                return redirect('next_gen_sms:manage_users')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    if search_query:
        users = CustomUser.objects.filter(username__icontains=search_query)
    else:
        users = CustomUser.objects.all()

    return render(request, 'next_gen_sms/manage_users.html', {'users': users, 'form': form, 'search_query': search_query})

@login_required
@user_passes_test(lambda u: u.is_admin())
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('next_gen_sms:manage_users')
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, 'next_gen_sms/edit_user.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_admin())
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('next_gen_sms:manage_users')
    return render(request, 'next_gen_sms/delete_user.html', {'user': user})

@login_required
def profile(request):
    return render(request, 'next_gen_sms/profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('next_gen_sms:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'next_gen_sms/update_profile.html', {'form': form})

@login_required
def update_profile_section(request):
    if request.method == 'POST':
        section = request.POST.get('section')
        # Implement logic to update specific profile section
        # This is a placeholder for partial updates
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
@user_passes_test(lambda u: u.is_admin())
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('login')
    return render(request, 'next_gen_sms/delete_account.html')