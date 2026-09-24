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