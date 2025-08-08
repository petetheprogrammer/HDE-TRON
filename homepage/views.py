import os
import tempfile
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import OCRUploadForm, ConfirmSerialForm
from utils.ocr import ocr_space_file
from .models import SerialRecord

@login_required
def home(request):
    # Initialize forms and variables
    ocr_form     = OCRUploadForm(request.POST or None, request.FILES or None)
    confirm_form = None
    parsed_text  = None
    raw_json     = None

    # Handle confirmation submission (from barcode scan)
    if request.method == 'POST' and 'serial_number' in request.POST:
        serial_number = request.POST.get('serial_number', '').strip()
        # Worker name automatically comes from logged-in user
        worker_name = request.user.username
        
        if serial_number:
            try:
                SerialRecord.objects.create(
                    serial_number=serial_number,
                    worker_name=worker_name,
                    uploader=request.user
                )
                messages.success(request, f'✅ Serial {serial_number} saved for {worker_name}!')
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Error saving: {str(e)}')
        else:
            messages.error(request, 'Serial number is required.')
    
    return render(request, 'homepage/home.html', {
        'ocr_form':     ocr_form,
        'confirm_form': confirm_form,
        'parsed_text':  parsed_text,
        'parsed':     json.dumps(raw_json, indent=2) if raw_json else None,
        'username': request.user.username,
    })

#logout view
def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/loginpage/')
