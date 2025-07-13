# utils/ocr.py
import requests

def ocr_space_file(filename, overlay=False, api_key='K85162163988957', language='eng'):
    """
    OCR.space API request with a local file.
    Returns the API’s JSON response as a Python dict.
    """
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    with open(filename, 'rb') as f:
        r = requests.post(
            'https://api.ocr.space/parse/image',
            files={ 'file': f },
            data=payload,
        )
    return r.json()
