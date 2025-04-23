from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from next_gen_sms.models import Certification
from next_gen_sms.forms import CertificationForm

@login_required
def upload_certification(request):
    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Certification uploaded successfully.')
            return redirect('next_gen_sms:certifications_view')
    else:
        form = CertificationForm()
    return render(request, 'certifications.html', {'form': form, 'certifications': Certification.objects.all(), 'is_admin': request.user.is_admin(), 'is_teacher': request.user.is_teacher()})

@login_required
def certifications_view(request):
    certifications = Certification.objects.all()
    return render(request, 'next_gen_sms/certifications_view.html', {'certifications': certifications})

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_teacher())
def delete_certification(request, cert_id):
    certification = get_object_or_404(Certification, id=cert_id)
    if request.method == 'POST':
        certification.delete()
        messages.success(request, 'Certification deleted successfully.')
        return redirect('next_gen_sms:certifications_view')
    return render(request, 'next_gen_sms/delete_certification.html', {'certification': certification})
