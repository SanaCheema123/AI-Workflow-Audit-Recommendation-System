# AI Workflow Audit & Recommendation System

An AI-powered full-stack application for auditing, evaluating, and improving automation and AI-agent workflows.

The system accepts workflow JSON files, analyzes their architecture and configuration, identifies reliability, security, governance, performance, scalability, and maintainability concerns, calculates an overall readiness score, and generates actionable recommendations.

The project combines a modern React frontend with a FastAPI backend, SQLite persistence, deterministic workflow analysis, and Gemini-assisted auditing.

---

## ✨ Key Features

- Create and manage workflow audit projects
- Upload workflow JSON files
- Analyze n8n-style automation and AI-agent workflows
- Structural workflow parsing and validation
- AI-assisted audit analysis using Google Gemini
- Deterministic rule-based auditing
- Overall workflow audit score
- Production-readiness assessment
- Risk-level classification
- Detailed audit findings
- Prioritized recommendations
- Workflow architecture metrics
- Audit report generation
- Audit history and management
- Interactive dashboard
- Responsive modern interface
- Light and dark workspace modes
- Global dynamic color themes
- Persistent UI preferences
- Backend health monitoring
- JSON report export

---

## 🖥️ Application Pages

### 1. Landing Page

The landing page introduces the workflow auditing platform through a modern product-style interface.

It includes:

- Product introduction
- 3D workflow/security illustrations
- Platform capabilities
- Workflow audit process
- Feature highlights
- Calls to action
- Responsive hero section

---

### 2. Dashboard

The dashboard provides an overview of workflow audit activity.

It displays information such as:

- Total audits
- Completed audits
- Average audit/readiness score
- Workflow statistics
- Risk distribution
- Recent audits
- Audit score trends
- Finding-category insights

The dashboard uses professional visualizations rather than basic administrative charts.

---

### 3. Audits

The Audits workspace provides access to previously created audits.

Users can:

- Browse audits
- Search audit projects
- Select an audit
- Review audit status
- View overall score
- Review risk level
- Check production readiness
- Inspect findings
- Review workflow structure
- Read recommendations
- Export reports
- Delete audits

---

### 4. New Audit

The New Audit workflow guides the user through the complete audit process.

Typical flow:

1. Create an audit project
2. Enter project information
3. Upload one or more workflow JSON files
4. Validate workflow structure
5. Start the audit
6. Analyze the workflow
7. Generate findings
8. Generate recommendations
9. Calculate readiness score
10. Review the completed audit

---

### 5. Settings

The Settings page provides UI and system preferences.

Available controls include:

- Light mode
- Dark mode
- Global color palette
- Compact interface density
- Auto-refresh preference
- Interface notifications
- Backend health check

Appearance preferences are stored locally because the backend currently focuses on workflow audit APIs rather than user preference persistence.

---

# 🧠 Audit Architecture

The auditing pipeline combines deterministic analysis with AI-assisted evaluation.

```text
Workflow JSON
     │
     ▼
Workflow Upload
     │
     ▼
JSON Validation
     │
     ▼
Workflow Parser
     │
     ├───────────────┐
     ▼               ▼
Structural        Rule-Based
Analysis          Audit Engine
     │               │
     └───────┬───────┘
             ▼
        Gemini Analysis
             │
             ▼
       Audit Findings
             │
             ▼
      Risk Assessment
             │
             ▼
      Recommendations
             │
             ▼
     Readiness Scoring
             │
             ▼
        Audit Report
```

---

# 🔍 Audit Areas

The system can evaluate workflow concerns across areas such as:

- Architecture
- Reliability
- Security
- AI Governance
- Performance
- Cost
- Scalability
- Observability
- Maintainability

The objective is to identify weaknesses before automation or AI workflows are considered production ready.

---

# 📊 Workflow Metrics

Uploaded workflows can be structurally analyzed for metrics such as:

- Total nodes
- Trigger nodes
- AI-related nodes
- Integrations
- Connections

These metrics provide context for both deterministic and AI-assisted analysis.

---

# ⚠️ Risk Assessment

Audit results can classify workflows according to their overall level of risk.

Typical classifications include:

- Low
- Medium
- High
- Critical

The calculated audit score also contributes to the production-readiness assessment.

---

# 🛠️ Technology Stack

## Frontend

- React
- Vite
- React Router
- Lucide React
- JavaScript
- CSS3
- Responsive CSS Grid/Flexbox
- CSS custom properties for global theming
- LocalStorage for interface preferences

## Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Pydantic Settings
- SQLite
- HTTPX
- Python Multipart
- Google GenAI SDK

## AI

- Google Gemini
- Configured model: `gemini-2.5-flash`

---

# 📁 Project Structure

```text
AI-Workflow-Audit/
│
├── backend/
│   │
│   ├── app/
│   │   ├── routes/
│   │   │   └── audits.py
│   │   │
│   │   ├── services/
│   │   │   ├── audit_service.py
│   │   │   ├── gemini_service.py
│   │   │   ├── rule_auditor.py
│   │   │   └── workflow_parser.py
│   │   │
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── storage/
│   ├── audit.db
│   └── .env
│
├── frontend/
│   │
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── context/
│   │   ├── lib/
│   │   ├── pages/
│   │   └── ...
│   │
│   ├── .env.example
│   ├── index.html
│   └── package.json
│
├── requirements.txt
└── README.md
```

---

# 🚀 Installation and Setup

## Prerequisites

Make sure the following are installed:

- Python 3.10+
- Node.js
- npm
- Git

---

# 1. Clone the Repository

```bash
git clone <your-repository-url>
cd AI-Workflow-Audit
```

If you already have the project locally, simply open the project folder in VS Code.

---


# 2. Backend Environment Configuration

The backend reads configuration from:

```text
backend/.env
```

A typical configuration is:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash

DATABASE_URL=sqlite:///./audit.db

MAX_UPLOAD_MB=25
STORAGE_DIR=storage

CORS_ORIGINS=http://localhost:5173
```

> Never commit your real API keys or secrets to GitHub.

It is recommended to keep `.env` in `.gitignore`.

---

# 4. Start the Backend

Move into the backend directory:

```bash
cd backend
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

The backend should run at:

```text
http://127.0.0.1:8000
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 5. Frontend Setup

Open another terminal.

Move into the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

---

# 6. Frontend Environment Configuration

Create:

```text
frontend/.env
```

or copy the existing `.env.example`.

Add:

```env
VITE_API_URL=http://127.0.0.1:8000
```

This connects the React application to the FastAPI backend.

---

# 7. Start the Frontend

Run:

```bash
npm run dev
```

Vite will normally start the application at:

```text
http://localhost:5173
```

Open this address in your browser.

---

# ▶️ Running the Full Application

Use two terminals.

## Terminal 1 — Backend

```bash
cd backend
uvicorn app.main:app --reload
```

## Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

# 🔌 Backend API

The frontend communicates with the following FastAPI endpoints.

## Health Check

```http
GET /health
```

Checks whether the API is operational.

---

## Create Audit

```http
POST /api/audits
```

Creates a new audit project.

Example request:

```json
{
  "project_name": "Customer Support Automation",
  "description": "Production readiness audit for an AI support workflow."
}
```

---

## List Audits

```http
GET /api/audits
```

Returns available audit projects.

---

## Get Audit

```http
GET /api/audits/{audit_id}
```

Returns detailed information about a specific audit.

---

## Upload Workflow

```http
POST /api/audits/{audit_id}/workflow
```

Uploads a workflow JSON file using multipart form data.

The uploaded file must be a valid `.json` workflow file.

---

## Start Audit

```http
POST /api/audits/{audit_id}/start
```

Starts analysis of the uploaded workflow.

---

## Get Findings

```http
GET /api/audits/{audit_id}/findings
```

Returns detected workflow issues.

---

## Get Recommendations

```http
GET /api/audits/{audit_id}/recommendations
```

Returns remediation and improvement recommendations.

---

## Get Report

```http
GET /api/audits/{audit_id}/report
```

Returns the complete audit report.

---

## Delete Audit

```http
DELETE /api/audits/{audit_id}
```

Deletes an audit project.

---

# 📄 Workflow Upload Format

The application is designed to inspect workflow JSON structures.

A workflow should contain a valid node structure such as:

```json
{
  "name": "Example Workflow",
  "nodes": [
    {
      "name": "Trigger",
      "type": "example-trigger"
    },
    {
      "name": "AI Processing",
      "type": "ai-agent"
    }
  ],
  "connections": {}
}
```

The actual structure can vary depending on the workflow platform and workflow being audited.

---

# 🤖 Gemini Integration

The backend can use Google Gemini to complement deterministic audit rules.

Configure the API key in:

```text
backend/.env
```

```env
GEMINI_API_KEY=your_api_key_here
```

The configured default model is:

```text
gemini-2.5-flash
```

Do not expose this key in frontend code.

All Gemini communication should remain server-side.

---

# 💾 Database

The project uses SQLite through SQLAlchemy.

The local database is:

```text
backend/audit.db
```

It stores audit-related application data such as:

- Audit projects
- Workflow metadata
- Findings
- Recommendations
- Scores
- Risk information
- Audit status

SQLite makes local development simple because no separate database server is required.

---

# 📂 Workflow Storage

Uploaded workflow files are stored under:

```text
backend/storage/
```

Audit-specific subdirectories are used to organize uploaded workflow files.

---

# 🔐 Security Recommendations

Before publishing or deploying the project:

- Never commit `.env`
- Never commit Gemini API keys
- Do not expose credentials in frontend code
- Validate uploaded files
- Restrict allowed CORS origins in production
- Use environment variables for production configuration
- Keep dependency versions maintained
- Do not publish sensitive workflow files
- Do not commit local database files containing sensitive information

Recommended `.gitignore` entries:

```gitignore
# Environment variables
.env
*.env
!.env.example

# Python
__pycache__/
*.py[cod]
.venv/
venv/

# Node
node_modules/
dist/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Local database
*.db

# Uploaded workflow storage
backend/storage/

# Logs
*.log
```

---

# 🏗️ Production Build

To create the frontend production build:

```bash
cd frontend
npm run build
```

The generated production files will be placed in the frontend build output directory used by Vite.

Preview the production build with:

```bash
npm run preview
```

---

# 🧪 API Testing

FastAPI provides interactive API documentation.

After starting the backend, open:

```text
http://127.0.0.1:8000/docs
```

From there you can test:

- Audit creation
- Audit retrieval
- Workflow upload
- Audit execution
- Findings
- Recommendations
- Reports
- Audit deletion

---

# 🎯 Project Objective

Modern automation workflows increasingly combine APIs, AI models, external services, triggers, data processing, and autonomous agents.

As workflow complexity increases, issues involving reliability, security, maintainability, governance, observability, cost, and production readiness become harder to identify manually.

The **AI Workflow Audit & Recommendation System** provides a centralized workflow assurance layer that analyzes workflow structure, identifies potential weaknesses, evaluates risk, and provides actionable recommendations before deployment.

---

# 🔮 Future Enhancements

Potential future improvements include:

- User authentication and authorization
- Role-based access control
- Organization workspaces
- PDF report generation
- Audit comparison
- Workflow version comparison
- Historical score tracking
- Advanced analytics
- Real-time workflow monitoring
- CI/CD integration
- GitHub integration
- Additional workflow platforms
- Custom audit policies
- Compliance templates
- Team collaboration
- Cloud deployment
- Production database support

---

# ⚠️ Important Note

This system performs workflow auditing and analysis.

It should not be interpreted as proof that a workflow is completely secure, compliant, reliable, or production safe.

AI-generated findings should be reviewed alongside deterministic checks and appropriate human technical review before production deployment.

---

## AI Workflow Audit & Recommendation System

**Analyze workflows. Identify risks. Improve architecture. Build production-ready automation.**