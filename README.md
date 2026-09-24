# AI-Powered Predictive Maintenance & Root Cause Analysis

An end-to-end Machine Learning and Generative AI system for predicting machine failures and providing AI-powered root-cause analysis using sensor data, RAG, embeddings, vector search, and a local LLM.

## Project Overview

The system combines traditional Machine Learning with Generative AI to analyze machine sensor readings.

It can:

- Predict whether a machine is likely to fail
- Estimate failure probability
- Retrieve relevant maintenance knowledge
- Generate root-cause analysis
- Recommend maintenance checks
- Expose the functionality through REST APIs
- Run automated tests through GitHub Actions
- Build a production-ready Docker image

## Architecture

```text
Machine Sensor Data
        |
        v
+----------------------+
| Random Forest Model  |
| Failure Prediction   |
+----------------------+
        |
        v
Failure Status +
Probability
        |
        +----------------------+
        |                      |
        v                      v
Maintenance Knowledge      Machine Readings
        |                      |
        v                      |
Embeddings + ChromaDB          |
        |                      |
        +----------+-----------+
                   |
                   v
              RAG Context
                   |
                   v
            Llama 3.2 / Ollama
                   |
                   v
          Root Cause Analysis
                   |
                   v
               FastAPI
                   |
                   v
             REST API Client


## Tech Stack

### Machine Learning
- Python
- NumPy
- Pandas
- Scikit-learn
- Random Forest
- PyTorch

### Generative AI
- Llama 3.2
- Ollama
- LangChain
- RAG
- Prompt Engineering

### NLP & Vector Search
- Transformers
- Sentence Transformers
- Embeddings
- ChromaDB
- Semantic Search

### Backend
- FastAPI
- Pydantic
- REST APIs

### DevOps & CI/CD
- Git
- GitHub
- GitHub Actions
- Docker
- GitHub Container Registry

API Endpoints

Health Check--GET /

Failure Prediction -- POST /predict

Example parameters:

temperature = 92
vibration = 8.5
pressure = 88
voltage = 2.9
operating_hours = 8500

Returns the predicted machine status and failure probability.

Maintenance Knowledge / RAG -- POST /ask

Complete Machine Analysis -- POST /analyze

Combines:

1.Machine sensor readings
2.ML failure prediction
3.Failure probability
4.Vector retrieval
5.LLM reasoning
6.Root-cause analysis
7.Recommended checks

                    Machine Learning
                    The project uses a Random Forest classifier for machine failure prediction.

            Input features:

Temperature
Vibration
Pressure
Voltage
Operating hours

RAG Pipeline

User Query
    ↓
Embedding Model
    ↓
Vector Search
    ↓
ChromaDB
    ↓
Relevant Maintenance Documents
    ↓
Prompt + Retrieved Context
    ↓
Llama 3.2
    ↓
Generated Response


CI/CD

GitHub Actions automatically:

Checks out the repository
Sets up Python
Installs dependencies
Runs API tests
Builds the Docker image
Publishes the container image to GitHub Container Registry

Run tests locally: python -m pytest

Running Locally
Create and activate the virtual environment: python -m venv venv
.\venv\Scripts\Activate.ps1

Install dependencies:pip install -r requirements.txt

Start the API:uvicorn src.api:app --reload

Open the API documentation: http://127.0.0.1:8000/docs

Local LLM

The project uses Ollama to run Llama 3.2 locally.

Make sure Ollama is running and the model is available:ollama run llama3.2

Project Structure

PredictiveMaintenanceAi/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── models/
│   └── failure_prediction_model.pkl
│
├── src/
│   ├── __init__.py
│   ├── api.py
│   └── train_model.py
│
├── tests/
│   └── test_api.py
│
├── data/
├── documents/
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md


Future Improvements

Real industrial sensor datasets
Model monitoring
Authentication and authorization
Cloud deployment
Advanced anomaly detection
Automated model retraining
Monitoring and observability
Production database integration