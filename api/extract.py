from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import PyPDF2
import docx

app = FastAPI()

def extract_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    content = ""

    if file.filename.endswith(".pdf"):
        content = extract_from_pdf(file.file)
    elif file.filename.endswith(".docx"):
        content = extract_from_docx(file.file)
    else:
        return JSONResponse({"error": "Formato não suportado"}, status_code=400)

    return {"filename": file.filename, "text": content}
