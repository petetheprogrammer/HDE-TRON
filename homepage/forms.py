# homepage/forms.py
from django import forms

class OCRUploadForm(forms.Form):
    image = forms.ImageField(label="Select image to OCR")
