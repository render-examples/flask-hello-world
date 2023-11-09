# import PyPDF2

# def load_pdf_content(filepath):

#   with open(filepath, 'rb') as f:
#     pdf = PyPDF2.PdfReader(f)
#     text = ''
#     for page in pdf.pages:
#       text += page.extract_text()

#   return text

import PyPDF2
import requests
from io import BytesIO

class ScrapPdf:

    def load_pdf_content(url):
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        with BytesIO(response.content) as f:
            pdf = PyPDF2.PdfReader(f)
            text = ''
            for page in pdf.pages:
                text += page.extract_text()

        return text

