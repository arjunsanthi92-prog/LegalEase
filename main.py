from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT
from xml.sax.saxutils import escape
import os
import time

load_dotenv()

app = FastAPI()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    effective_date: str


@app.get("/")
def home():
    return {
        "message": "LegalEase Backend is Working"
    }


@app.post("/generate")
def generate_document(request: DocumentRequest):

    prompt = f"""
    Create a simple legal document.

    Document type: {request.document_type}
    Parties: {request.parties}
    Terms: {request.terms}
    Effective date: {request.effective_date}

    Generate the document in clear and formal language.
    """

    try:

        for attempt in range(3):

            try:
                print(f"Trying Gemini... Attempt {attempt + 1}")

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                print("Gemini response received!")

                # Create PDF
                pdf_path = "generated_document.pdf"

                styles = getSampleStyleSheet()
                style = styles["Normal"]
                style.alignment = TA_LEFT
                style.fontSize = 11
                style.leading = 16

                doc = SimpleDocTemplate(
                    pdf_path,
                    pagesize=A4,
                    rightMargin=50,
                    leftMargin=50,
                    topMargin=50,
                    bottomMargin=50
                )

                story = []

                for line in response.text.split("\n"):
                    line = line.strip()

                    if line:
                        story.append(
                            Paragraph(escape(line), style)
                        )
                        story.append(Spacer(1, 8))

                doc.build(story)

                print("PDF created successfully!")

                return FileResponse(
                    path=pdf_path,
                    media_type="application/pdf",
                    filename="LegalEase_Document.pdf"
                )

            except Exception as e:

                print("Gemini Error:", e)

                if attempt < 2:
                    print("Waiting 5 seconds...")
                    time.sleep(5)
                else:
                    return {
                        "error": str(e)
                    }

    except Exception as e:

        return {
            "error": str(e)
        }