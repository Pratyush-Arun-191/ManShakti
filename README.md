# ManShakti

## AI-Powered Student Wellbeing & Academic Insight Platform

ManShakti is an AI-powered platform designed to help educational institutions
identify hidden student wellbeing concerns and academic learning gaps through
natural language.

The platform connects students, teachers, and timely human support through
AI-assisted insights.

---

## Problem

In large classrooms, teachers may not always be able to identify:

- Students experiencing prolonged academic pressure
- Students who hesitate to communicate their difficulties
- Hidden wellbeing concerns
- Concepts that students have misunderstood
- Learning gaps that may not be visible through marks alone

Traditional academic performance indicators often show the outcome, but not
the underlying reason.

---

## Solution

ManShakti combines two complementary modules.

### 1. Student Wellbeing Monitoring

Students complete a daily reflection:

> "How was your day today?"

The reflection is processed using an LLM to extract structured wellbeing
indicators.

These features are then passed to a machine learning model that estimates
the student's current stress level.

ManShakti also considers recent prediction history rather than reacting to
one difficult day.

If concerning predictions persist across multiple days, the system generates
a support alert for human review.

### 2. Academic Understanding Analysis

Students answer subjective questions in their own words.

The AI evaluates:

- Understanding level
- Missing concepts
- Feedback
- Recommended learning topic

The student can then search for resources related to the identified concept.

---

## System Workflow

```text
Student Input
     |
     +----------------------+
     |                      |
     v                      v
Wellbeing Reflection    Academic Answer
     |                      |
     v                      v
Gemini LLM             Gemini LLM
     |                      |
     v                      v
Structured Features    Understanding Analysis
     |
     v
Machine Learning Model
     |
     v
Recent History Analysis
     |
     +----------+
                |
                v
        Teacher Insights
                |
                v
          Human Review
```

---

## Key Features

### Student

- Daily wellbeing reflection
- AI-powered wellbeing analysis
- Stress-pattern monitoring
- Subjective academic assessment
- Concept-gap identification
- Learning resource recommendation

### Teacher

- Class-level student insights
- Academic understanding indicators
- Concept-gap visibility
- Wellbeing indicators
- Persistent-pattern review alerts
- Human-in-the-loop support

---

## Technology Stack

### Frontend

- React
- Vite
- CSS

### Backend

- Python
- FastAPI
- Uvicorn

### Database

- PostgreSQL

### AI

- Google Gemini
- Natural language processing
- Structured feature extraction

### Machine Learning

- Scikit-learn
- Random Forest
- Joblib

---

## Machine Learning Pipeline

The wellbeing model uses the following features:

- Anxiety level
- Self-esteem
- Living conditions
- Basic needs
- Academic performance
- Study load
- Teacher-student relationship
- Future career concerns
- Social support
- Peer pressure
- Extracurricular activities
- Bullying

The model predicts a stress level from 0 to 2.

The current prototype achieved approximately **87% accuracy** on the held-out
test set of the selected dataset.

---

## Privacy & Human-in-the-Loop

ManShakti is designed as a decision-support system rather than an autonomous
diagnostic system.

Important principles:

- The system does not diagnose mental health conditions.
- A single difficult day does not automatically trigger an alert.
- Recent patterns are considered before generating a support alert.
- AI-generated insights are intended for human review.
- Sensitive detailed reflections should be restricted to authorized roles in
  a production implementation.

---

## Current Prototype Scope

This hackathon prototype demonstrates:

- Student interaction
- AI analysis
- Machine learning prediction
- PostgreSQL storage
- Multi-day wellbeing analysis
- Academic concept-gap analysis
- Teacher insight dashboard

The prototype focuses on demonstrating the core workflow rather than
production-scale deployment.

---

## Future Scope

Potential future improvements include:

- Secure authentication and role-based access control
- Field-level privacy controls
- Multilingual NLP
- Mobile application
- LMS/ERP integration
- Attendance and academic analytics
- More comprehensive wellbeing models
- Institutional-scale deployment
- Audit logging and stronger data protection

---

## Project Structure

```text
Prototype/
├── backend/
│   ├── main.py
│   ├── ml/
│   │   ├── feature_extraction_prompt.py
│   │   ├── process_features.py
│   │   ├── predict_wellbeing.py
│   │   ├── save_prediction.py
│   │   ├── get_prediction_history.py
│   │   ├── check_student_history.py
│   │   ├── history_analysis.py
│   │   └── wellbeing_model.pkl
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   └── package.json
│
└── README.md
```

---

## Running the Project

### Prerequisites

Make sure the following are installed:

- Python
- Node.js and npm
- PostgreSQL

### 1. Start PostgreSQL

Create the `man_shakti` database and configure the database connection in the
backend environment file.

The backend expects environment variables similar to:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/man_shakti
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Do not commit real credentials or API keys to the repository.

### 2. Start the Backend

Navigate to:

```text
backend
```

Activate the Python virtual environment and run:

```bash
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Start the Frontend

Open another terminal and navigate to:

```text
frontend
```

Install dependencies if required:

```bash
npm install
```

Run:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## API Overview

The prototype exposes FastAPI endpoints for:

- Student creation and retrieval
- Reflection submission
- Wellbeing analysis
- Reflection history
- Academic answer evaluation

The interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## Important Note

ManShakti is a hackathon prototype intended to demonstrate the concept and
technical workflow.

AI-generated wellbeing indicators and ML predictions should not be
interpreted as medical diagnoses or definitive assessments of a student's
mental health.

The prototype uses AI-assisted analysis and machine learning as decision
support. Any real-world intervention should involve appropriate human review,
privacy safeguards, and qualified institutional professionals.

---

## Future Vision

ManShakti aims to bridge the gap between student voice, academic
understanding, and timely institutional support by turning natural-language
student input into actionable insights while keeping humans in the loop.