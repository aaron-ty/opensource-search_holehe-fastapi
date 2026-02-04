---

# Sfera OSINT Service

**High-performance OSINT backend for email and phone intelligence.**
Automates reconnaissance across 200+ platforms, providing structured, reliable results for security, fraud detection, and compliance workflows.

---

## Overview

Sfera is a production-ready service designed to handle **high-volume intelligence queries** at scale. It supports:

* **Email reconnaissance:** Detects if emails are registered across 150+ platforms (social media, forums, services).
* **Phone reconnaissance:** Checks phone numbers across multiple platforms.
* **Orchestrated processing:** Automatically routes queries and determines data type for maximum efficiency.
* **Standardized API:** Returns consistent, predictable JSON responses for downstream systems.

Sfera is **built for reliability, scalability, and maintainability**. Its architecture separates concerns across API, domain logic, and infrastructure modules.

---

## Key Features

* **Parallelized multi-source queries** for faster, more accurate results
* **Automated type detection** and query routing
* **Role-based access control and secure API endpoints**
* **AI-assisted orchestration** for intelligent workflow handling
* **Full Docker support** for reproducible dev and production environments

---

## Architecture

```
sfera-osint-service/
├── src/
│   ├── api/v1/              # FastAPI endpoints for email, phone, orchestrator
│   ├── controllers/         # Request handling & orchestration logic
│   ├── domain/              # Business rules, models, and services
│   ├── infrastructure/      # Integrations with OSINT modules & validators
│   └── core/                # Configuration, logging, constants
├── main.py                  # Application entry
└── requirements.txt
```

**Design Principles:**

* **Domain-Driven Design:** Keeps business logic separate from infrastructure and API layers.
* **Microservices-ready:** Can be scaled horizontally with minimal coupling.
* **Observability:** Structured logging, monitoring hooks, and error tracking built in.

---

## Technology Stack

* **Backend:** Python 3.11, FastAPI, Pydantic
* **Recon Engines:** Holehe (email), Ignorant (phone)
* **Infrastructure:** AWS (S3, EC2, Lambda), Docker, Kubernetes
* **Testing & Quality:** TDD, integration tests, CI/CD pipelines

---

## Deployment

### Local Development

```bash
git clone https://github.com/aaron-ty/sfera-osint-service.git
cd sfera-osint-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker (Recommended)

```bash
docker-compose -f docker-compose.dev.yml up --build
docker-compose -f docker-compose.prod.yml up --build -d
```

---

## API Highlights

Sfera exposes **three main endpoints**:

1. **Email Search (`POST /api/v2/email/search`)**
2. **Phone Search (`POST /api/v2/phone/search`)**
3. **Orchestrator (`POST /api/v2/orchestrator/search`)** – handles mixed queries with automatic type detection

All endpoints return structured JSON with metadata, query results, and error handling. Includes **rate-limit handling, validation errors, and service availability responses**.

**Example Response:**

```json
{
  "query": "example@gmail.com",
  "results": {
    "gravatar": {"status": "ok", "found": true},
    "twitter": {"status": "error", "code": 429}
  },
  "successful_queries": 1,
  "failed_queries": 1
}
```

---

## Why This Project Matters

Sfera isn’t a proof-of-concept. It’s a **production-grade system** designed to handle real-world security and compliance needs:

* **Scalable** – Handles hundreds of queries per second
* **Reliable** – Full logging, retries, and error handling
* **Secure** – JWT authentication, RBAC for endpoint access
* **Extensible** – New OSINT modules can be added without touching core orchestration

---

## Who Should Use This

* Security and fraud teams needing real-time OSINT checks
* Compliance engineers requiring automated data verification
* Backend engineers exploring scalable orchestration patterns

---

## Next Steps / Contribution

* Add new OSINT modules for emerging platforms
* Extend orchestrator to handle bulk queries asynchronously
* Integrate monitoring dashboards for metrics and error rates

---
