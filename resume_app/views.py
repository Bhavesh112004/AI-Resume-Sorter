from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ResumeUploadForm
from django.core.exceptions import ValidationError
from pdfminer.high_level import extract_text
from .nlp_pipeline import preprocess_text
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import PyPDF2
# Ensure match_jobs_to_candidate is imported correctly from utils
from .utils import extract_basic_info, extract_skills, match_roles, match_jobs_to_candidate
from .models import Job
import os
import re
import mammoth
import tempfile

# --- Helper Functions ---

def allowed_file(file):
    valid_extensions = ['pdf', 'doc', 'docx']
    file_extension = os.path.splitext(file.name)[1][1:].lower()
    if file_extension not in valid_extensions:
        raise ValidationError("Invalid file format. Please upload a PDF, DOC, or DOCX file.")
    return True

def clean_extracted_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^a-zA-Z0-9@.,\s\-]', '', text)
    return text

def ocr_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def extract_text_from_resume(resume_path, file_extension):
    try:
        extracted_text = ''
        if file_extension == 'pdf':
            reader = PyPDF2.PdfReader(resume_path)
            if reader.is_encrypted:
                return None
            extracted_text = extract_text(resume_path)
            if not extracted_text.strip() or len(extracted_text.strip()) < 50:
                extracted_text = ocr_pdf(resume_path)
        elif file_extension in ['doc', 'docx']:
            with open(resume_path, "rb") as docx_file:
                result = mammoth.extract_raw_text(docx_file)
                extracted_text = result.value
        else:
            return None
        return clean_extracted_text(extracted_text)
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

# --- Main Views ---

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_instance = form.save()
            resume_file = resume_instance.resume_file
            file_extension = os.path.splitext(resume_file.name)[1][1:].lower()

            try:
                allowed_file(resume_file)
            except ValidationError as e:
                return JsonResponse({"response": str(e)})

            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
                    for chunk in resume_file.chunks():
                        temp_file.write(chunk)
                    temp_resume_path = temp_file.name

                text = extract_text_from_resume(temp_resume_path, file_extension)
                os.remove(temp_resume_path)

                if not text:
                    return JsonResponse({"response": "Failed to extract text from the resume."})

                # NLP processing using imported utils
                info = extract_basic_info(text)
                extracted_skills = extract_skills(text)

                # Match against database jobs
                all_jobs = Job.objects.all()
                job_matches = match_jobs_to_candidate(extracted_skills, all_jobs)

                return render(request, 'resume_app/results.html', {
                    "name": info['name'],
                    "email": info['email'],
                    "phone": info['phone'],
                    "skills": extracted_skills,
                    "job_matches": job_matches,
                    "extracted_text": text[:1000],
                })

            except Exception as e:
                return JsonResponse({"response": f"Error processing resume: {e}"})
    else:
        form = ResumeUploadForm()

    return render(request, 'resume_app/upload.html', {'form': form})

def success(request):
    return render(request, 'resume_app/success.html')