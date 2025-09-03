from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
import docx

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "API Python rodando no Render 🚀"}

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    content = ""
    if file.filename.endswith(".pdf"):
        pdf = PdfReader(file.file)
        for page in pdf.pages:
            content += page.extract_text() or ""
    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        for para in doc.paragraphs:
            content += para.text + "\n"
    else:
        content = "Formato não suportado"
    return {"text": content}
