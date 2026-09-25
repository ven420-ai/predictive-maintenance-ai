from urllib import response

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
# import chromadb
import os
from google import genai
# from sentence_transformers import SentenceTransformer
from torchgen import context
import time



app = FastAPI(title="Predictive Maintenance AI")


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Load ML model
# -----------------------------
model = joblib.load("models/failure_prediction_model.pkl")


# -----------------------------
# Load embedding model
# -----------------------------
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# # -----------------------------
# # Connect to ChromaDB
# # -----------------------------
# client = chromadb.PersistentClient(path="vector_db")
# collection = client.get_or_create_collection(
#     name="maintenance_knowledge"
# )


# -----------------------------
# Local LLM
# -----------------------------
import os
from google import genai

gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# -----------------------------
# Request format
# -----------------------------
class Question(BaseModel):
    query: str


class MachineData(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    voltage: float
    operating_hours: int

# -----------------------------
# Home
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Predictive Maintenance AI API is running"
    }


# -----------------------------
# ML Prediction
# -----------------------------
@app.post("/predict")
def predict(machine_data: MachineData):

    machine = pd.DataFrame({
        "temperature": [machine_data.temperature],
        "vibration": [machine_data.vibration],
        "pressure": [machine_data.pressure],
        "voltage": [machine_data.voltage],
        "operating_hours": [machine_data.operating_hours]
    })

    prediction = model.predict(machine)[0]
    probability = model.predict_proba(machine)[0][1]

    return {
        "prediction": "FAILURE" if prediction == 1 else "NORMAL",
        "failure_probability": round(float(probability), 4)
    }


# -----------------------------
# RAG retrieval
# -----------------------------
maintenance_knowledge = [
    "High machine temperature can indicate cooling system degradation, blocked airflow, or cooling fan failure.",
    "Excessive machine vibration can indicate motor bearing wear, shaft misalignment, or mechanical imbalance.",
    "Low voltage can indicate power supply problems and unstable machine operation.",
    "Low operating pressure can indicate hydraulic leakage, pump problems, or pressure regulator failure.",
    "High operating hours increase the possibility of component wear and maintenance requirements.",
    "Cooling fan failure can cause temperature to rise rapidly.",
    "Abnormal motor bearing vibration can indicate bearing wear or mechanical damage.",
    "Power supply fluctuations can cause electronic components to behave incorrectly."
]

def retrieve_context(query, n_results=3):
    query_words = set(query.lower().split())

    scored = []

    for doc in maintenance_knowledge:
        doc_words = set(doc.lower().split())
        score = len(query_words.intersection(doc_words))
        scored.append((score, doc))

    scored.sort(reverse=True)

    return [doc for score, doc in scored[:n_results]]




# -----------------------------
# GenAI / RAG endpoint
# -----------------------------
@app.post("/ask")
def ask(question: Question):

    context = retrieve_context(question.query)

    context_text = "\n".join(
        f"- {doc}" for doc in context
    )

    prompt = f"""
You are a machine maintenance AI assistant.

Answer using the provided maintenance knowledge.

Knowledge:
{context_text}

Question:
{question.query}

Give a concise answer with likely cause and recommended checks.
"""

    response = gemini_client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    answer = response.text

    return {
        "question": question.query,
        "answer": answer,
        "sources": context
    }


@app.post("/analyze")
def analyze(machine_data: MachineData):

    machine = pd.DataFrame({
        "temperature": [machine_data.temperature],
        "vibration": [machine_data.vibration],
        "pressure": [machine_data.pressure],
        "voltage": [machine_data.voltage],
        "operating_hours": [machine_data.operating_hours]
    })

    prediction = model.predict(machine)[0]
    probability = model.predict_proba(machine)[0][1]

    status = "FAILURE" if prediction == 1 else "NORMAL"

    query = f"""
    Machine temperature {machine_data.temperature},
    vibration {machine_data.vibration},
    pressure {machine_data.pressure},
    voltage {machine_data.voltage},
    operating hours {machine_data.operating_hours}.
    What could cause this machine condition?
    """

    context = retrieve_context(query, n_results=3)

    context_text = "\n".join(
        f"- {doc}" for doc in context
    )

    prompt = f"""
You are a machine maintenance AI assistant.

Use the machine readings exactly as provided.
Do not invent normal ranges.
Do not contradict the ML prediction.

Machine readings:
Temperature: {machine_data.temperature}°C
Vibration: {machine_data.vibration}
Pressure: {machine_data.pressure}
Voltage: {machine_data.voltage}V
Operating hours: {machine_data.operating_hours}

ML prediction:
Status: {status}
Failure probability: {probability:.2%}

Maintenance knowledge:
{context_text}

Analyze the machine.

Provide:
1. Machine status
2. Likely root cause
3. Which readings may indicate a problem
4. Evidence from the maintenance knowledge
5. Recommended checks
"""

    answer = None

    for attempt in range(3):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            answer = response.text
            break

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)

    if answer is None:
        answer = (
            "AI analysis is temporarily unavailable. "
            "The ML prediction and retrieved maintenance knowledge "
            "are still available."
        )

    return {
        "machine_data": machine_data.dict(),
        "status": status,
        "failure_probability": round(float(probability), 4),
        "analysis": answer,
        "sources": context
    }