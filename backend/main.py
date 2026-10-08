from fastapi import FastAPI

app = FastAPI(
    title="AI What Went Wrong? - Incident Detective",
    description="Backend API for analyzing incidents using AI",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "incident-detective"
    }