# homepage/views.py
import os, tempfile, json
from django.conf import settings
from django.shortcuts import render
from .forms import OCRUploadForm
from utils.ocr import ocr_space_file

def home(request):
    parsed_text = None
    raw_json = None

    if request.method == 'POST':
        form = OCRUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data['image']
            suffix = os.path.splitext(img.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                for chunk in img.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            try:
                result = ocr_space_file(
                    filename=tmp_path,
                    overlay=False,
                    api_key=settings.OCR_SPACE_API_KEY,
                    language='eng'
                )
                raw_json = result
                parsed = result.get('ParsedResults')
                if parsed and parsed[0].get('ParsedText'):
                    parsed_text = parsed[0]['ParsedText'].strip()
                else:
                    parsed_text = 'No text detected.'
            finally:
                os.remove(tmp_path)
    else:
        form = OCRUploadForm()

    return render(request, 'homepage/home.html', {
        'form': form,
        'parsed_text': parsed_text,
        'raw_json': json.dumps(raw_json, indent=2) if raw_json else None,
    })
