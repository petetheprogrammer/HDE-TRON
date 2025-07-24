# homepage/forms.py
from django import forms

class OCRUploadForm(forms.Form):
    image = forms.ImageField(label="Select image to OCR")
    
    def clean_image(self):
        img = self.cleaned_data.get('image')
        if img and img.size > 1024 * 1024:  # 1 MB
            raise forms.ValidationError("File too large (max 1 MB).")
        return img

class ConfirmSerialForm(forms.Form):
    serial_number = forms.CharField(
        max_length=100,
        label="Serial Number",
        help_text="Edit if OCR made a mistake"
    )
    worker_name = forms.CharField(
        max_length=100,
        label="Employee Name",
        help_text="Edit if OCR made a mistake"
    )