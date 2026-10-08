from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

from gemma.gemma_service import analyze_incident


app = FastAPI(
    title="AI What Went Wrong? - Incident Detective",
    description="Backend API for analyzing incidents using AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "incident-detective"
    }


@app.post("/investigate")
async def investigate(
    image: UploadFile = File(...),
    context: str = Form(...)
):
    # Create a temporary file for the uploaded image
    file_extension = os.path.splitext(image.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=file_extension
    ) as temp_file:

        image_data = await image.read()
        temp_file.write(image_data)
        temp_image_path = temp_file.name

    try:
        # Send image + context to Gemma
        evidence = analyze_incident(
            temp_image_path,
            context
        )

        return {
            "status": "success",
            "evidence": evidence
        }

    finally:
        # Remove temporary image
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)