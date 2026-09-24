from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import chromadb

from sentence_transformers import SentenceTransformer
from langchain_ollama import ChatOllama


app = FastAPI(title="Predictive Maintenance AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# Connect to ChromaDB
# -----------------------------
client = chromadb.PersistentClient(path="vector_db")
collection = client.get_or_create_collection(
    name="maintenance_knowledge"
)


# -----------------------------
# Local LLM
# -----------------------------
import os

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)


# -----------------------------
# Request format
# -----------------------------
class Question(BaseModel):
    query: str


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
def predict(
    temperature: float,
    vibration: float,
    pressure: float,
    voltage: float,
    operating_hours: int
):
    machine = pd.DataFrame({
        "temperature": [temperature],
        "vibration": [vibration],
        "pressure": [pressure],
        "voltage": [voltage],
        "operating_hours": [operating_hours]
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
def retrieve_context(query, n_results=3):

    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    return results["documents"][0]


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

Answer the user's question using the maintenance
knowledge retrieved from the knowledge base.

Knowledge:
{context_text}

User question:
{question.query}

Give a clear answer and mention the likely cause
and recommended checks when appropriate.
"""

    response = llm.invoke(prompt)

    return {
        "question": question.query,
        "answer": response.content,
        "sources": context
    }


class MachineData(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    voltage: float
    operating_hours: int


@app.post("/analyze")
def analyze(machine_data: MachineData):

    # -----------------------------
    # 1. ML prediction
    # -----------------------------
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




    # -----------------------------
    # 2. RAG retrieval
    # -----------------------------
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


    # -----------------------------
    # 3. LLM analysis
    # -----------------------------
    prompt = f"""
You are a machine maintenance AI assistant.

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
3. Evidence from the readings
4. Recommended checks
"""

    response = llm.invoke(prompt)


    # -----------------------------
    # 4. Final response
    # -----------------------------
    return {
        "status": status,
        "failure_probability": round(float(probability), 4),
        "analysis": response.content,
        "sources": context
    }