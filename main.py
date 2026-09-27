from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="AI-powered educational assistant",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ---------------------------------------------------------
# Request Models
# ---------------------------------------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class QARequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500
    )


# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# ---------------------------------------------------------
# Q&A
# ---------------------------------------------------------

@app.post("/qa")
def qa(payload: QARequest):

    try:

        answer = answer_question(
            payload.question
        )

        return {
            "answer": answer
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# ---------------------------------------------------------
# Explain Topic
# ---------------------------------------------------------

@app.post("/explain")
def explain(payload: TextRequest):

    try:

        explanation = explain_topic(
            payload.text
        )

        return {
            "explanation": explanation
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# ---------------------------------------------------------
# Generate Quiz
# ---------------------------------------------------------

@app.post("/quiz")
def quiz(payload: QuizRequest):

    try:

        return generate_quiz(
            payload.text
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# ---------------------------------------------------------
# Summarize
# ---------------------------------------------------------

@app.post("/summarize")
def summarize(payload: TextRequest):

    try:

        summary = summarize_text(
            payload.text
        )

        return {
            "summary": summary
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# ---------------------------------------------------------
# Learning Path
# ---------------------------------------------------------

@app.post("/learn/recommendations")
def learning_path(
    payload: LearningPathRequest
):

    try:

        recommendations = get_learning_recommendations(
            payload.topic
        )

        return {
            "recommendations": recommendations
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )