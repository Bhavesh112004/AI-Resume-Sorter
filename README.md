# NLP-Based AI Resume Sorter & Analyzer

A professional **Natural Language Processing (NLP)** and **Optical Character Recognition (OCR)** system designed to automate and optimize the recruitment workflow. This project parses resumes in multiple formats, cleanses text using linguistic preprocessing, and ranks candidates based on semantic relevance to job descriptions.


## 🚀 Key Features

* **Intelligent OCR Extraction**: Utilizes `Tesseract OCR` and `pdf2image` to accurately extract text from scanned PDFs and image-based documents.
* **NLP-Driven Preprocessing**: Implements `NLTK` for deep text cleaning, including tokenization and stop-word removal.
* **Universal Document Support**: Seamlessly handles `.pdf`, `.docx`, and `.txt` files using `pdfminer.six` and `mammoth`.
* **Secure Configuration**: Uses `python-dotenv` to isolate sensitive credentials like `SECRET_KEY`, ensuring industry-standard security.
* **Automated Ranking**: Scores resumes against job requirements to identify top talent instantly.

---

## 🛠️ Tech Stack

* **Framework**: Django (Python)
* **NLP Library**: NLTK (Natural Language Toolkit)
* **OCR Engine**: Tesseract OCR (via PyTesseract)
* **File Handling**: PDFMiner.six, Mammoth, PyPDF2, Pillow, pdf2image
* **Environment Management**: Python-Dotenv


## 🧠 How It Works (The Logic)

1. **Data Ingestion**: The system accepts PDF, DOCX, and Image files.
2. **Text Extraction Pipeline**:
   - **Digital PDFs**: Extracted via `pdfminer.six`.
   - **Scanned Documents**: Converted to images via `pdf2image`, then processed using `Tesseract OCR`.
3. **NLP Processing Pipeline**:
   - **Tokenization**: Breaking text into individual words using `NLTK`.
   - **Stop-word Removal**: Filtering out non-essential words (e.g., "is", "the").
   - **Semantic Cleaning**: Normalizing case and removing special characters.
4. **Scoring Engine**: Compares the processed resume tokens against job description keywords to generate a match percentage.



---

## 📦 Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/Bhavesh112004/NLP-Resume-Intelligence.git](https://github.com/Bhavesh112004/NLP-Resume-Intelligence.git)
    cd NLP-Resume-Intelligence
    ```

2.  **Initialize Virtual Environment**:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    Create a `.env` file in the root directory (same folder as `manage.py`):
    ```text
    SECRET_KEY=your_secure_django_key
    DEBUG=True
    ```

5.  **Initialize Database & Download NLP Data**:
    ```bash
    python manage.py migrate
    python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords')"
    ```

---

## 🗺️ Roadmap & Future Enhancements
- [ ] **UI/UX Overhaul**: Transitioning from Django Templates to a modern React-based frontend.
- [ ] **LLM Integration**: Implementing Llama 3 or GPT-4 for nuanced candidate feedback.
- [ ] **Skill Visualization**: Adding Chart.js dashboards for applicant skill distribution.
- [ ] **API Documentation**: Implementing Swagger/OpenAPI for third-party integrations.

---

## 👨‍💻 Author

**Bhavesh**
* **GitHub**: [@Bhavesh112004](https://github.com/Bhavesh112004)
* **Role**: Computer Engineer | Pune, Maharashtra
* **Focus**: AI/ML, Scalable Web Architecture
