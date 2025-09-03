from fastapi import FastAPI
from pydantic import BaseModel
from PyPDF2 import PdfReader
import docx
import base64
import io

app = FastAPI()

class FileData(BaseModel):
    filename: str   # Nome do ficheiro (ex: "cv.pdf")
    content: str    # Conteúdo do ficheiro em base64

@app.get("/")
def home():
    return {"msg": "API Python rodando no Render 🚀"}

@app.post("/extract")
async def extract(file: FileData):
    content = ""
    try:
        # Decodifica base64
        decoded = base64.b64decode(file.content)

        # Processa PDF
        if file.filename.endswith(".pdf"):
            pdf = PdfReader(io.BytesIO(decoded))
            for page in pdf.pages:
                content += page.extract_text() or ""

        # Processa DOCX
        elif file.filename.endswith(".docx"):
            doc = docx.Document(io.BytesIO(decoded))
            for para in doc.paragraphs:
                content += para.text + "\n"

        else:
            content = "Formato não suportado"

    except Exception as e:
        return {"error": str(e)}

    return {"text": content}
