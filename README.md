
# 🔍 Sfera OSINT Service

A high-performance OSINT (Open-Source Intelligence) service for email and phone number reconnaissance across multiple platforms. This service provides automated checks across 200+ social media platforms, websites, and services to determine if specific email addresses or phone numbers are registered.

## 🚀 What It Does

- **Email Intelligence**: Check email registration across 150+ platforms (social media, forums, services)
- **Phone Intelligence**: Verify phone number presence across multiple platforms
- **Multi-Source Verification**: Parallel checks across multiple data sources
- **Standardized API**: Consistent Sfera-compliant response format
- **Orchestrated Processing**: Automatic data type detection and routing

## 🛠 Technology Stack

- **FastAPI** - Modern, high-performance web framework
- **Python 3.11** - Core programming language
- **Holehe** - Email reconnaissance engine
- **Ignorant** - Phone number reconnaissance engine
- **Pydantic** - Data validation and settings management
- **Domain-Driven Design** - Clean, maintainable architecture

## 📁 Project Structure detailed tree is on program_tree.txt

```
sfera-osint-service/ 
├── src/
│   ├── api/v1/              # API endpoints
│   │   ├── email.py         # Email search endpoints
│   │   ├── phone.py         # Phone search endpoints
│   │   └── orchestrator.py  # Multi-query processing
│   ├── controllers/         # Request handlers
│   │   ├── email_controller.py
│   │   ├── phone_controller.py
│   │   └── orchestrator_controller.py
│   ├── domain/              # Business logic
│   │   ├── models/          # Data models
│   │   ├── services/        # Core services
│   │   └── exceptions.py    # Custom exceptions
│   ├── infrastructure/      # External integrations
│   │   ├── http/            # HTTP clients
│   │   ├── modules/         # OSINT modules
│   │   └── validators/      # Data validation
│   └── core/                # Configuration & utilities
│       ├── config.py        # App settings
│       ├── constants.py     # Constants
│       └── logging.py       # Logging setup
├── main.py                  # Application entry point
└── requirements.txt         # Dependencies
```

# ⚙️ Running the Service

## Start with Uvicorn (local)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

# 🐳 Running with Docker (recommended for stability)

## Development

```bash
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up
# or detached:
docker-compose -f docker-compose.dev.yml up -d
```

## Production

```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up
# or detached:
docker-compose -f docker-compose.prod.yml up -d
```

---

# 💻 Local Installation

1. Create virtual environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Provide `.env` file
4. Start the server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

# 🔐 Environment Variables

Create `.env`, `.env.dev`, or `.env.prod`:

```env
VALIDATOR_URL=http://your-validator-service/api/v1
SERVICE_NAME=opensource_search_holehe_fastapi
MODE=dev

```

---


# 🌐 Complete API Documentation - Remaining Endpoints
## 🩺 **Health & Status Endpoints**

### **1. Root Endpoint**
**URL:** `GET /`  
**Method:** `GET`  
**Description:** Service information

**Response:**
```json
{
  "service": "holehe-service",
  "version": "2.0.0",
  "status": "running"
}
```

---

### **2. Health Check**
**URL:** `GET /health`  
**Method:** `GET`  
**Description:** Health check endpoint

**Response:**
```json
{
  "headers": {
    "sender": "sfera.core"
  },
  "body": {
    "status": "ok",
    "version": "2.0.0",
    "service": "holehe-service"
  },
  "extra": {
    "timestamp": "2025-11-20T16:55:26+00:00",
    "mode": "production"
  }
}
```

**Errors:**
- `503 Service Unavailable` - Service unhealthy

---

### **3. Status Check**
**URL:** `GET /status`  
**Method:** `GET`  
**Description:** Status check endpoint

**Response:**
```json
{
  "headers": {
    "sender": "sfera.core"
  },
  "body": {
    "status": "ok",
    "version": "2.0.0",
    "service": "holehe-service"
  },
  "extra": {
    "timestamp": "2025-11-20T16:55:26+00:00",
    "mode": "production"
  }
}
```

---

## ⚠️ **Common Error Responses**

### **Validation Error (400)**
```json
{
  "headers": {"sender": "sfera.core"},
  "body": {
    "error": "Invalid request data",
    "details": [
      {
        "loc": ["body", "payload"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ],
    "status": "error",
    "code": 400
  },
  "extra": {
    "timestamp": "2025-11-20T16:55:26+00:00",
    "path": "/api/v2/email/search"
  }
}
```

### **Rate Limit Error (429)**
```json
{
  "headers": {"sender": "sfera.email"},
  "body": {
    "error": "Rate limit exceeded for module: twitter",
    "status": "error",
    "code": 429
  },
  "extra": {
    "timestamp": "2025-11-20T16:55:26+00:00",
    "retry_after": 60
  }
}
```

### **Internal Server Error (500)**
```json
{
  "headers": {"sender": "sfera.core"},
  "body": {
    "error": "Internal server error",
    "status": "error",
    "code": 500
  },
  "extra": {
    "timestamp": "2025-11-20T16:55:26+00:00",
    "error_id": "err_5f3a2b1c"
  }
}
```

### **Service Unavailable (503)**
```json
{
  "headers": {"sender": "sfera.core"},
  "body": {
    "error": "Service temporarily unavailable",
    "status": "error", 
    "code": 503
  },
  "extra": {
    "timestamp": "2025-11-20T16:55:26+00:00",
    "retry_after": 300
  }
}
```

---
## 📧 **Email Endpoints**

### **1. Get Active Email Modules**
**URL:** `GET /api/v2/email/modules/active`  
**Method:** `GET`  
**Description:** Get list of active email modules

**Response:**
```json
{
  "headers": {
    "sender": "sfera.email"
  },
  "body": {
    "modules": ["gravatar", "adobe", "twitter", "instagram"],
    "count": 150,
    "type": "email"
  },
  "extra": {
    "timestamp": "2025-11-20T16:55:26+00:00"
  }
}
```

**Errors:**
- `500 Internal Server Error` - Service unavailable

---

### **2. Get All Email Modules**
**URL:** `GET /api/v2/email/modules/all`  
**Method:** `GET`  
**Description:** Get list of all email modules (active + inactive)

**Response:**
```json
{
  "headers": {
    "sender": "sfera.email"
  },
  "body": {
    "modules": ["gravatar", "adobe", "twitter", "inactive_module"],
    "count": 200,
    "type": "email"
  },
  "extra": {
    "timestamp": "2025-11-20T16:55:26+00:00"
  }
}
```

**Errors:**
- `500 Internal Server Error` - Service unavailable

---

### **3. Search Email**
**URL:** `POST /api/v2/email/search`  
**Method:** `POST`  
**Description:** Search for email across multiple modules

**Payload:**
```json
{
  "payload": "example@gmail.com",
  "modules": ["gravatar", "adobe", "twitter"]
}
```

```json
# for all modules:

{
  "modules": [
    "*"
  ],
  "payload": "example@gmail.com"
}
```

**Query Parameters:**
- `only_found`: boolean (optional) - Return only modules with found data

**Response:**
```json
{
  "headers": {
    "sender": "sfera.email"
  },
  "body": {
    "query": "example@gmail.com",
    "total_modules": 3,
    "successful": 2,
    "failed": 1,
    "results": {
      "gravatar": {
        "status": "ok",
        "code": 200,
        "message": "ok",
        "records": [
          {
            "result": "Найден",
            "result_code": "FOUND",
            "email_recovery": "backup@gmail.com"
          }
        ],
        "timestamp": "2025-11-20T16:55:26+00:00"
      },
      "adobe": {
        "status": "ok",
        "code": 200,
        "message": "ok",
        "records": [
          {
            "result": "Найден",
            "result_code": "FOUND",
            "phone_number": "+1234567890"
          }
        ],
        "timestamp": "2025-11-20T16:55:26+00:00"
      },
      "twitter": {
        "status": "error",
        "code": 429,
        "message": "Rate limit exceeded",
        "records": [],
        "timestamp": "2025-11-20T16:55:26+00:00"
      }
    }
  },
  "extra": {
    "timestamp": "2025-11-20T16:55:26+00:00",
    "data_type": "email",
    "query_type": "email_search"
  }
}
```

**Errors:**
- `400 Bad Request` - Invalid email format or module name
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Service error
- `503 Service Unavailable` - Module temporarily unavailable

---

## 📱 **Phone Endpoints**

### **1. Get Active Phone Modules**
**URL:** `GET /api/v2/phone/modules/active`  
**Method:** `GET`  
**Description:** Get list of active phone modules

**Response:**
```json
{
  "headers": {
    "sender": "sfera.phone"
  },
  "body": {
    "modules": ["instagram", "snapchat", "amazon"],
    "count": 3,
    "type": "phone"
  },
  "extra": {
    "timestamp": "2025-11-20T16:34:50+00:00"
  }
}
```

**Errors:**
- `500 Internal Server Error` - Service unavailable

---

### **2. Get All Phone Modules**
**URL:** `GET /api/v2/phone/modules/all`  
**Method:** `GET`  
**Description:** Get list of all phone modules

**Response:**
```json
{
  "headers": {
    "sender": "sfera.phone"
  },
  "body": {
    "modules": ["instagram", "snapchat", "amazon", "inactive_module"],
    "count": 4,
    "type": "phone"
  },
  "extra": {
    "timestamp": "2025-11-20T16:34:50+00:00"
  }
}
```

**Errors:**
- `500 Internal Server Error` - Service unavailable

---

### **3. Search Phone**
**URL:** `POST /api/v2/phone/search`  
**Method:** `POST`  
**Description:** Search for phone number across multiple modules

**Payload:**
```json
{
  "payload": "79208533738",
  "modules": ["instagram", "snapchat"]
}
```
or

```json
# for all modules:

{
  "modules": [
    "*"
  ],
  "payload": "79208533738"
}
```

**Query Parameters:**
- `only_found`: boolean (optional) - Return only modules with found data

**Response:**
```json
{
  "headers": {
    "sender": "sfera.phone"
  },
  "body": {
    "query": "79208533738",
    "total_modules": 2,
    "successful": 1,
    "failed": 1,
    "results": {
      "instagram": {
        "status": "ok",
        "code": 200,
        "message": "ok",
        "records": [
          {
            "result": "Найден",
            "result_code": "FOUND",
            "username": "john_doe",
            "profile_url": "https://instagram.com/john_doe"
          }
        ],
        "timestamp": "2025-11-20T16:55:26+00:00"
      },
      "snapchat": {
        "status": "ok",
        "code": 204,
        "message": "No data found",
        "records": [],
        "timestamp": "2025-11-20T16:55:26+00:00"
      }
    }
  },
  "extra": {
    "timestamp": "2025-11-20T16:55:26+00:00",
    "data_type": "phone",
    "query_type": "phone_search"
  }
}
```

**Errors:**
- `400 Bad Request` - Invalid phone format or module name
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Service error
- `503 Service Unavailable` - Module temporarily unavailable

---

## 🎛️ **Orchestrator Endpoints**

### **1. Orchestrator Search (With Validator)**
**URL:** `POST /api/v2/orchestrator/search`  
**Method:** `POST`  
**Description:** Main orchestrator endpoint that automatically detects data types using validator service

**Payload:**
```json
{
  "queries": ["example@gmail.com", "79208533738", "invalid_data"]
}
```

**Response:**
```json
{
  "headers": {
    "sender": "sfera.orchestrator"
  },
  "body": {
    "total_queries": 3,
    "processed_queries": 3,
    "successful_queries": 2,
    "failed_queries": 1,
    "results": [
      {
        "headers": {"sender": "sfera.email.gravatar"},
        "body": {
          "query": "example@gmail.com",
          "module": "gravatar",
          "status": "ok",
          "found": true,
          "records": [{"result": "Найден", "result_code": "FOUND"}]
        },
        "extra": {
          "timestamp": "2025-11-20T16:55:26+00:00",
          "data_type": "email"
        }
      },
      {
        "headers": {"sender": "sfera.phone.instagram"},
        "body": {
          "query": "79208533738",
          "module": "instagram",
          "status": "ok",
          "found": true,
          "records": [{"result": "Найден", "result_code": "FOUND"}]
        },
        "extra": {
          "timestamp": "2025-11-20T16:55:26+00:00",
          "data_type": "phone"
        }
      },
      {
        "headers": {"sender": "sfera.orchestrator"},
        "body": {
          "query": "invalid_data",
          "error": "Unsupported data type: unknown",
          "status": "error",
          "code": 400
        },
        "extra": {
          "timestamp": "2025-11-20T16:55:26+00:00",
          "supported_types": ["email", "phone"]
        }
      }
    ]
  },
  "extra": {
    "timestamp": "2025-11-20T16:55:26+00:00",
    "validation_source": "validator",
    "service_version": "2.0.0"
  }
}
```

**Errors:**
- `400 Bad Request` - Invalid request format
- `500 Internal Server Error` - Service error
- `503 Service Unavailable` - Validator service unavailable

---

### **2. Direct Search (Without Validator)**
**URL:** `POST /api/v2/orchestrator/search-direct`  
**Method:** `POST`  
**Description:** Direct search that bypasses validator service

**Payload:**
```json
{
  "queries": ["test@example.com", "+79123456789"]
}
```

**Response:**
```json
{
  "headers": {
    "sender": "sfera.orchestrator"
  },
  "body": {
    "total_queries": 2,
    "processed_queries": 2,
    "successful_queries": 2,
    "failed_queries": 0,
    "results": [
      {
        "headers": {"sender": "sfera.email.gravatar"},
        "body": {
          "query": "test@example.com",
          "module": "gravatar",
          "status": "ok",
          "found": true,
          "records": [{"result": "Найден", "result_code": "FOUND"}]
        },
        "extra": {
          "timestamp": "2025-11-20T16:55:26+00:00",
          "data_type": "email"
        }
      },
      {
        "headers": {"sender": "sfera.phone.instagram"},
        "body": {
          "query": "+79123456789",
          "module": "instagram",
          "status": "ok",
          "found": false,
          "records": []
        },
        "extra": {
          "timestamp": "2025-11-20T16:55:26+00:00",
          "data_type": "phone"
        }
      }
    ]
  },
  "extra": {
    "timestamp": "2025-11-20T16:55:26+00:00",
    "validation_source": "direct",
    "service_version": "2.0.0"
  }
}
```

**Errors:**
- `400 Bad Request` - Invalid request format
- `500 Internal Server Error` - Service error

---
```
