from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm
from .models import CustomUser

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_users(request):
    """
    Admin view for managing user accounts and permissions.
    """
    print(f"User authenticated: {request.user.is_authenticated}")  # Debug auth
    print(f"User is admin: {request.user.is_admin()}")  # Debug role
    print(f"Request method: {request.method}")  # Debug method
    print(f"User ID: {request.user.id}, Username: {request.user.username}")  # Debug user info
    
    if request.method == 'POST':
        print("Form submitted with data:", request.POST)  # Debug form data
        form = CustomUserCreationForm(request.POST)
        print("Form errors:", form.errors)  # Debug errors
        if form.is_valid():
            print("Form is valid - creating user")  # Debug
            user = form.save(commit=False)
            try:
                user.save()
                print(f"User created successfully: {user.username}")  # Debug
                messages.success(request, f'User {user.username} created!')
                return redirect('next_gen_sms:manage_users')
            except Exception as e:
                print(f"Error saving user: {str(e)}")  # Debug error
                messages.error(request, f'Error creating user: {str(e)}')
    
    else:
        form = CustomUserCreationForm()

    # Get all users and paginate
    users = CustomUser.objects.all().order_by('date_joined')
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print("Page Object Contents:", page_obj)  # Debugging line to check contents
    print("Total Users Retrieved:", users.count())  # Debug total users
    print("Form:", form)  # Debugging line to check form

    return render(request, 'manage_users.html', {
        'form': form,
        'page_obj': page_obj
    })
