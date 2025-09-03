import json
import PyPDF2
import docx
from io import BytesIO

def extract_from_pdf(file_bytes):
    reader = PyPDF2.PdfReader(BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

def extract_from_docx(file_bytes):
    doc = docx.Document(BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs])

def handler(request):
    try:
        # Vercel envia o body cru
        body = request.body
        filename = request.headers.get("x-filename", "cv.pdf")

        if filename.endswith(".pdf"):
            text = extract_from_pdf(body)
        elif filename.endswith(".docx"):
            text = extract_from_docx(body)
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Formato não suportado"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"filename": filename, "text": text})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
