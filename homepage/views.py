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

    # Step 1: Handle confirmation submission
    if request.method == 'POST' and 'serial_number' in request.POST and 'worker_name' in request.POST:
        confirm_form = ConfirmSerialForm(request.POST)
        if confirm_form.is_valid():
            SerialRecord.objects.create(
                serial_number=confirm_form.cleaned_data['serial_number'],
                worker_name=confirm_form.cleaned_data['worker_name'],
                uploader=request.user
            )
            messages.success(request, '✅ Serial saved!')
            return redirect('home')

    # Step 2: Process camera or file upload
    elif request.method == 'POST':
        # Check for camera capture first, then file upload
        upload = request.FILES.get('camera_image') or request.FILES.get('file_image')
        if upload:
            # Enforce 1 MB limit
            if upload.size > 1024 * 1024:
                messages.error(request, 'File too large (max 1 MB).')
            else:
                # Write upload to a temporary file
                suffix = os.path.splitext(upload.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    for chunk in upload.chunks():
                        tmp.write(chunk)
                    tmp_path = tmp.name
                try:
                    # Call the OCR.space API
                    result = ocr_space_file(
                        filename=tmp_path,
                        overlay=False,
                        api_key=settings.OCR_SPACE_API_KEY,
                        language='eng'
                    )
                    raw_json   = result
                    text_block = result.get('ParsedResults', [{}])[0].get('ParsedText', '').strip()
                    parsed_text= text_block

                    # Parse SN and worker name
                    lines = [line.strip() for line in text_block.splitlines() if line.strip()]
                    sn = ''
                    for line in lines:
                        if line.lower().startswith('sn'):
                            parts = line.split(':', 1)
                            sn = parts[1].strip() if len(parts) > 1 else line.strip()
                            break
                    worker = lines[-1] if len(lines) >= 2 else ''

                    # Pre-fill confirmation form
                    confirm_form = ConfirmSerialForm(initial={
                        'serial_number': sn,
                        'worker_name':   worker,
                    })
                finally:
                    os.remove(tmp_path)

    return render(request, 'homepage/home.html', {
        'ocr_form':     ocr_form,
        'confirm_form': confirm_form,
        'parsed_text':  parsed_text,
        'parsed':     json.dumps(raw_json, indent=2) if raw_json else None,
    })
