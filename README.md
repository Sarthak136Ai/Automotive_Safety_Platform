# AutoSentinel AI — Explainable Automotive Recall Intelligence Platform

AutoSentinel AI is a production-grade, high-integrity safety intelligence platform designed for regulators, vehicle engineers, and manufacturing executives. By integrating advanced machine learning, deep natural language processing, and robust functional safety protocols, AutoSentinel AI converts raw vehicle recall complaints and campaign logs into actionable, explainable predictive intelligence.

The application is deployed as a highly responsive, glassmorphic **Single Page Application (SPA)** mounted directly inside an asynchronous **FastAPI** backend, serving all analytics, ML forecasters, vector similarity explorers, and dataset download streams on a single port (**`http://localhost:8000`**).

---

## 🏗️ System Architecture

AutoSentinel AI utilizes a dual-engine architecture served on a single port:
1. **Predictive Engine**: An input safety defect goes through standard feature cleaning, gets combined text vectorized (TF-IDF), transforms categorical and numeric dimensions, predicts class probabilities using XGBoost, and generates live feature contribution trace maps using a custom TreeExplainer SHAP engine.
2. **Semantic Engine**: Uses `all-MiniLM-L6-v2` dense embeddings generated over 5,000 safety recall logs. Incoming natural language queries are vectorized and compared using cosine-similarity to locate the most similar archived campaigns.
3. **ISO 26262 Override Layer**: Conforming to automotive functional safety standards, a heuristic safety override layer intercepts classifier metrics, automatically escalating high-severity occurrences (such as battery melting or complete loss of steering) to Critical/High risk tiers.

```mermaid
graph TD
    User([User Web Browser]) -->|Accesses http://localhost:8000| StaticServer[FastAPI StaticFiles Mount]
    StaticServer -->|Serves Static Assets| SPA[Sleek Single Page Application]
    SPA -->|Interactive Fetch Requests| Router[FastAPI Routers]
    Router -->|Assessment Forecaster| PredictAPI[/api/predict]
    Router -->|Brand Risk Stats| MfrAPI[/api/manufacturers]
    Router -->|Vector Comparison| SearchAPI[/api/search]
    Router -->|Dataset Download| DownloadAPI[/api/download/dataset]
    
    PredictAPI -->|Inference & Explanations| Models[ML/NLP Core Singletons]
    MfrAPI -->|Dynamic SQL Groups| SQLiteDB[(SQLite Database)]
    SearchAPI -->|Embedding Similarities| SQLiteDB
    DownloadAPI -->|Streams Structured CSV| CSVFile[ml_ready_vehicle_recalls.csv]
```

---

## ✨ Key Capabilities

* **📊 Executive Dashboard**: Displays total campaigns, Average Safety Risk Index, critical volume gauges, interactive top-risk brand charts (Chart.js), component failure breakdowns, and a searchable brand threat rankings table.
* **🔮 Recall Risk Predictor**: Evaluates natural language defect prompts using an XGBoost multiclass model, displays interactive radial match gauges, distribution probabilities, extracted SpaCy component entities, and direct **SHAP explanation waterfalls** (identifying specific tokens escalating or mitigating risk).
* **🔍 Semantic Search Explorer**: Leverages SentenceTransformer dense vector spaces to scan and retrieve historical campaigns matching natural language queries, with cosine similarity percentages and collapsible detail logs.
* **💡 Single-Click Defect Templates**: Includes a grid of 4 NLP presets (Tesla Battery, Honda Brakes, Ford Airbags, Toyota Engine) and 5 semantic presets to execute assessments instantly without typing.
* **💾 About Platform & Data Stream**: Features a dedicated technical summary page with a visual pipeline flowchart and a premium download trigger that directly streams the preprocessed **8.1 MB structured CSV safety dataset** from the server.

---

## 🔌 API Reference

AutoSentinel AI exposes a robust set of REST API endpoints:

### 1. Risk Assessment Forecaster
* **Endpoint**: `POST /api/predict`
* **Request Body**:
  ```json
  {
    "manufacturer": "Honda",
    "component": "Brakes",
    "model_year": 2021,
    "summary": "Brake master cylinder is leaking brake fluid at the piston seal.",
    "consequence": "Low hydraulic pressure causes soft brake pedal feel and increased stopping distances.",
    "remedy": "Dealers will replace the master cylinder assembly free of charge."
  }
  ```
* **Response**: Returns predicted risk tier (`Low`, `Medium`, `High`, `Critical`), classification probability distributions, SpaCy extracted components and failures, a BART-CNN summarizer headline, and token-level **SHAP feature contribution values**.

### 2. Brand Ratings & Aggregations
* **Endpoint**: `GET /api/manufacturers`
* **Response**: Returns a ranked list of manufacturers ordered by our custom **Safety Risk Index** (calculated from database recall distributions, severity ratios, and scale metrics).

### 3. High-Dimensional Semantic Search
* **Endpoint**: `POST /api/search`
* **Request Body**:
  ```json
  {
    "query": "steering wheel locking up unexpectedly",
    "top_k": 5
  }
  ```
* **Response**: Returns the top $K$ semantically related historical recalls matching the query, with cosine similarity scores, risk labels, and collapsible hazard summaries.

### 4. Safety Dataset Download
* **Endpoint**: `GET /api/download/dataset`
* **Response**: Streams `data/processed/ml_ready_vehicle_recalls.csv` directly to the client as an attachment, with absolute path resolution to guarantee delivery.

### 5. API Health Check
* **Endpoint**: `GET /api/health`
* **Response**: Displays service state, ML model load state, and vector engine readiness.

---

## 📦 Getting Started & Local Run

### Prerequisites
* **Python 3.10+** (Virtual environment setup inside `.venv` is recommended).
* **SQLite 3** (The platform automatically initializes and populates the SQLite database `autosentinel.db` with 5,000 campaigns on first startup).

### 1. Setup Virtual Environment and Dependencies
First, activate the Python virtual environment and install all core libraries, model runtimes, and the SpaCy NLP lightweight model:
```powershell
# Activate virtual environment (Windows Powershell)
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Download lightweight SpaCy english parser
python -m spacy download en_core_web_sm
```

### 2. Launch FastAPI Server
Run the FastAPI application from the project root. This mounts static files and boots all singletons (XGBoost, SHAP Explainer, and SentenceTransformers):
```powershell
# Start server in unbuffered mode (runs on http://localhost:8000)
.venv\Scripts\python.exe -u backend/app/main.py
```
Open **`http://localhost:8000`** in your browser to experience the AutoSentinel AI web application!

---

## 📓 Jupyter Notebook Modeling Sandbox

For researchers and data scientists, the full exploratory data analysis (EDA), data cleaning, text preprocessing, model fitting, and vector embeddings generation workflow are documented in our interactive sandbox:
* **Location**: [notebooks/autosentinel_ml_pipeline.ipynb](file:///c:/Users/hp/OneDrive/Desktop/Automotive_Safety_Platform/notebooks/autosentinel_ml_pipeline.ipynb)

To launch the modeling sandbox locally:
```powershell
# Spin up Jupyter Notebook server
.venv\Scripts\jupyter notebook notebooks/autosentinel_ml_pipeline.ipynb
```

---

## 🐳 Docker Containerization (Production Build)

To deploy AutoSentinel AI in a containerized environment (multi-container Postgres, FastAPI, and compiled React served by Nginx):

```bash
# Build and spin up orchestrated containers
docker-compose up --build
```
* **Web Client Dashboard**: Access the compiled React client served by Nginx at **`http://localhost`**
* **FastAPI Backend Swagger**: Explore and test REST endpoints at **`http://localhost:8000/docs`**
