# High-Level Design (HLD) Document
## Freeform Text Generation for Content Creators

## 1. INTRODUCTION

### 1.1 Purpose
This High-Level Design document provides a comprehensive overview of the Freeform Text Generation system architecture, components, interfaces, and design decisions. It serves as a blueprint for the implementation and maintenance of the AI-powered content generation platform.

### 1.2 Scope
This document covers:
- System architecture and component design
- Data flow and processing pipelines
- Technology stack and infrastructure
- Interface specifications
- Security and performance considerations
- Module interactions and dependencies

### 1.3 Intended Audience
- Development team members
- Project stakeholders
- System administrators
- Technical reviewers
- Future maintainers

### 1.4 Document Conventions
- **Bold text**: Important concepts and terms
- `Code style`: File names, functions, and technical terms
- *Italic text*: Emphasis and references

---

## 2. SYSTEM OVERVIEW

### 2.1 Project Background
The Freeform Text Generation platform is an AI-powered content creation tool designed for content creators, marketers, educators, and professionals who require high-quality, keyword-optimized long-form articles. The system leverages Llama 3.1-8B-Instant model through Groq API, combined with custom DCKG (Domain-Constrained Keyword Generation) and DMK (Domain-aware Model for Keyword enforcement) algorithms to ensure relevant, keyword-rich content generation.

### 2.2 System Objectives
- Generate long-form content (750-2000 words) in under 10 seconds
- Achieve 100% keyword enforcement accuracy
- Provide real-time quality metrics and performance analytics
- Deliver an engaging, cyberpunk-themed user experience
- Ensure scalability for multiple concurrent users
- Maintain high reliability and availability

### 2.3 Key Features
1. **AI-Powered Generation**: Llama 3.1 model for high-quality text
2. **Intelligent Keyword Extraction**: Domain-agnostic DCKG algorithm
3. **Guaranteed Keyword Enforcement**: Two-phase DMK validation
4. **Real-time Metrics**: Response time, accuracy, and quality scores
5. **Cyberpunk UI**: Engaging neon-themed interface
6. **Flexible Configuration**: Customizable word count and domain
7. **Download Functionality**: Export content as text files
8. **Comprehensive Logging**: JSON-based metrics tracking

---

## 3. SYSTEM ARCHITECTURE

### 3.1 Architectural Pattern
The system follows a **Three-Tier Architecture** pattern:

```
┌────────────────────────────────────────────────────────────────┐
│                     PRESENTATION TIER                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Streamlit Web Interface                     │  │
│  │  • User input forms (prompt, domain, word count)         │  │
│  │  • Cyberpunk-themed UI with CSS styling                  │  │
│  │  • Real-time metrics dashboard                           │  │
│  │  • Download functionality                                │  │
│  │  • Error handling and user feedback                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                              ↕ HTTP/REST
┌────────────────────────────────────────────────────────────────┐
│                      APPLICATION TIER                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 FastAPI Backend Server                   │  │
│  │  • Request validation and processing                     │  │
│  │  • DCKG module (keyword extraction)                      │  │
│  │  • DMK module (keyword enforcement)                      │  │
│  │  • Metrics calculation engine                            │  │
│  │  • Response formatting and cleanup                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                              ↕ HTTPS/JSON
┌────────────────────────────────────────────────────────────────┐
│                      INTEGRATION TIER                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Groq API (Llama 3.1 Model)                  │  │
│  │  • Text generation engine                                │  │
│  │  • 8 billion parameter model                             │  │
│  │  • High-speed inference                                  │  │
│  │  • Token-based processing                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                              ↕
┌────────────────────────────────────────────────────────────────┐
│                        DATA TIER                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              JSON File Storage System                    │  │
│  │  • generation_logs.json (individual generations)         │  │
│  │  • final_metrics_report.json (aggregate metrics)         │  │
│  │  • Environment variables (.env)                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### 3.2 Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                    │
└─────────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────────┐
│  FRONTEND (longform_streamlit.py)                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Input Forms  │  │ UI Components│  │ HTTP Client  │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────────┐
│  BACKEND (llama_api.py)                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ FastAPI App  │  │ API Endpoints│  │Request Handler│          │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ DCKG Module  │  │  DMK Module  │  │Groq API Client│          │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────────┐
│  PROCESSING MODULES                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   dckg.py    │  │   dmk.py     │  │test_results.py│          │
│  │  (Keywords)  │  │(Enforcement) │  │  (Metrics)    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────────┐
│  EXTERNAL SERVICES                                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Groq API (Llama 3.1-8B-Instant)                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. DATA FLOW ARCHITECTURE

### 4.1 Request Flow Diagram

```
┌─────────┐
│  USER   │
└────┬────┘
     │ 1. Enter prompt, domain, word count
     ↓
┌─────────────────────┐
│ STREAMLIT FRONTEND  │
│  • Validate input   │
│  • Start timer      │
└────┬────────────────┘
     │ 2. POST /generate
     ↓
┌─────────────────────┐
│  FASTAPI BACKEND    │
│  • Receive request  │
└────┬────────────────┘
     │ 3. Extract keywords
     ↓
┌─────────────────────┐
│   DCKG MODULE       │
│  • Parse prompt     │
│  • Score terms      │
│  • Return keywords  │
└────┬────────────────┘
     │ 4. Enhance prompt
     ↓
┌─────────────────────┐
│   DMK MODULE        │
│  • Add keyword inst.│
│  • Format prompt    │
└────┬────────────────┘
     │ 5. Calculate tokens
     │    tokens = (words/0.75)*1.3
     ↓
┌─────────────────────┐
│   GROQ API CLIENT   │
│  • Build request    │
│  • Send to API      │
└────┬────────────────┘
     │ 6. Generate text
     ↓
┌─────────────────────┐
│  LLAMA 3.1 MODEL    │
│  • Process prompt   │
│  • Generate content │
└────┬────────────────┘
     │ 7. Return generated text
     ↓
┌─────────────────────┐
│  FASTAPI BACKEND    │
│  • Clean text       │
│  • Validate keywords│
└────┬────────────────┘
     │ 8. Calculate metrics
     ↓
┌─────────────────────┐
│ METRICS MODULE      │
│  • Response time    │
│  • Keyword accuracy │
│  • Enforcement rate │
│  • Length metrics   │
└────┬────────────────┘
     │ 9. Log results
     ↓
┌─────────────────────┐
│ JSON STORAGE        │
│  • Save generation  │
│  • Update aggregates│
└────┬────────────────┘
     │ 10. Return response
     ↓
┌─────────────────────┐
│ STREAMLIT FRONTEND  │
│  • Display content  │
│  • Show metrics     │
│  • Enable download  │
└────┬────────────────┘
     │ 11. Content ready
     ↓
┌─────────┐
│  USER   │
└─────────┘
```

### 4.2 Data Processing Pipeline

**Stage 1: Input Processing**
- User provides: prompt, domain, desired word count
- Frontend validates input completeness
- Timer starts for response time measurement

**Stage 2: Keyword Extraction (DCKG)**
- Tokenize prompt into words
- Remove stopwords
- Extract unigrams and bigrams
- Apply scoring: frequency × length × capitalization × phrase boosts
- Select top 10 keywords

**Stage 3: Prompt Enhancement (DMK Pre-Generation)**
- Create structured instruction template
- Insert user prompt
- Add keyword requirements (single words and phrases)
- Include quality guidelines
- Format as comprehensive generation instruction

**Stage 4: Token Calculation**
- Convert word count to token estimate
- Formula: `max_tokens = (max_words / 0.75) * 1.3`
- 0.75 = average words per token
- 1.3 = 30% buffer to prevent cut-offs

**Stage 5: AI Generation**
- Send enhanced prompt to Groq API
- Llama 3.1-8B-Instant processes request
- Model generates content based on instructions
- Return generated text

**Stage 6: Post-Processing**
- Clean generated text
- Remove incomplete final sentences
- Trim whitespace

**Stage 7: Keyword Validation (DMK Post-Generation)**
- Check keyword presence in generated text
- Calculate keyword density
- Analyze distribution across text sections
- Assess context quality
- Generate quality metrics

**Stage 8: Metrics Calculation**
- Response time: `end_time - start_time`
- Keyword accuracy: overlap between prompt and generated keywords
- Keyword enforcement: percentage of required keywords present
- Word count accuracy: actual words vs. requested
- Unique word ratio: unique words / total words

**Stage 9: Logging and Storage**
- Create generation record with all metrics
- Append to `generation_logs.json`
- Update aggregate metrics in `final_metrics_report.json`

**Stage 10: Response Delivery**
- Package generated text and metrics
- Return to frontend
- Display in user interface
- Enable download option

---

## 5. MODULE SPECIFICATIONS

### 5.1 Frontend Module (longform_streamlit.py)

**Purpose**: Provide user interface for content generation

**Key Components**:
1. **Configuration**
   - Page title and layout settings
   - Cyberpunk CSS styling
   - Color scheme and typography

2. **Input Section**
   - Text area for prompt (multi-line)
   - Text input for domain
   - Slider for word count (100-2000)

3. **Action Buttons**
   - Generate button with glow effects
   - Download button for content export

4. **Display Section**
   - Generated content text area
   - Metrics expander with detailed statistics
   - Status messages and errors

**Technologies**:
- Streamlit framework
- Custom CSS for styling
- Requests library for API calls
- Time module for performance tracking

**Key Functions**:
- `make_api_request()`: Send generation request to backend
- Timer logic: Measure end-to-end response time
- Metrics display: Show detailed performance data
- Download handler: Create .txt file for export

### 5.2 Backend Module (llama_api.py)

**Purpose**: Handle API requests and orchestrate content generation

**Key Components**:
1. **FastAPI Application**
   - POST endpoint: `/generate`
   - Request validation with Pydantic
   - Response formatting

2. **Request Processing**
   - Extract prompt, domain, word count
   - Invoke DCKG for keyword extraction
   - Invoke DMK for prompt enhancement

3. **AI Integration**
   - Groq API client setup
   - Token calculation logic
   - System prompt configuration
   - Error handling for API failures

4. **Response Handling**
   - Text cleanup
   - DMK validation
   - Quality metrics packaging
   - Error responses

**Technologies**:
- FastAPI framework
- Pydantic for data validation
- Requests library for Groq API
- Python-dotenv for configuration
- Logging module

**Key Functions**:
- `generate()`: Main endpoint handler
- Token calculation: `(max_words / 0.75) * 1.3`
- API communication with Groq
- Validation and cleanup

### 5.3 DCKG Module (dckg.py)

**Purpose**: Extract relevant keywords from user prompts

**Algorithm Overview**:
1. Text preprocessing (lowercase, tokenization)
2. Stopword removal
3. Unigram and bigram extraction
4. Intelligent scoring with multiple boosts
5. Top-N keyword selection

**Scoring Factors**:
- **Frequency Boost**: `1 + (freq - 1) * 0.2`
- **Length Boost**: `1 + (len - 4) * 0.08`
- **Capitalization Boost**: `1.4` for capitalized words
- **Phrase Boost**: `2.0` for bigrams

**Key Features**:
- Domain-agnostic (no hardcoded word lists)
- Context-aware scoring
- Multi-word phrase detection
- Adaptive to any topic

**Function Signature**:
```python
def generate_keywords(prompt: str, domain: str, top_n: int = 10) -> List[str]
```

### 5.4 DMK Module (dmk.py)

**Purpose**: Enforce keyword presence in generated content

**Two-Phase Approach**:

**Phase 1: Pre-Generation**
- Enhance user prompt with keyword instructions
- Create structured template with requirements
- Separate single keywords and phrases
- Add quality guidelines

**Phase 2: Post-Generation**
- Validate keyword presence
- Calculate keyword density
- Analyze distribution across text sections
- Assess context quality
- Generate comprehensive metrics

**Quality Metrics**:
- `total_keywords`: Number of required keywords
- `present_keywords`: Count of keywords found
- `keyword_density`: Percentage of text that is keywords
- `well_distributed`: Keywords across text sections
- `context_quality`: Keywords in meaningful sentences

**Function Signatures**:
```python
# Pre-generation
def apply_dmk_loss(prompt: str, keywords: List[str]) -> str

# Post-generation
def apply_dmk_loss(prompt: str, keywords: List[str], 
                   generated_text: str) -> Tuple[bool, List[str], Dict]
```

### 5.5 Metrics Module (test_results.py)

**Purpose**: Calculate, log, and aggregate performance metrics

**Key Functions**:

1. **extract_keywords()**: Simple frequency-based keyword extraction
2. **keyword_accuracy()**: Calculate overlap percentage
3. **keyword_enforcement()**: Check keyword presence percentage
4. **length_metrics()**: Analyze word count accuracy
5. **analyze_generation()**: Complete single-generation analysis
6. **log_generation()**: Save results to JSON
7. **aggregate_metrics()**: Calculate averages across all generations
8. **final_report()**: Generate comprehensive report

**Metrics Tracked**:
- Response time (seconds)
- Keyword accuracy (percentage)
- Keyword enforcement (percentage)
- Word count accuracy (percentage)
- Unique word ratio (percentage)
- Target achievement flags

**Storage Format**:
```json
{
  "timestamp": "ISO-8601 datetime",
  "prompt_keywords": ["list of extracted keywords"],
  "generated_keywords": ["list from generated text"],
  "keyword_accuracy%": 70.0,
  "keyword_enforcement%": 100.0,
  "response_time_s": 4.46,
  "length_metrics": {
    "requested": 750,
    "actual": 972,
    "accuracy%": 129.6,
    "unique%": 35.49,
    "target_met": false
  }
}
```

---

## 6. TECHNOLOGY STACK

### 6.1 Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | Streamlit | 1.30.0+ | Web interface framework |
| **Backend** | FastAPI | Latest | REST API server |
| **Language** | Python | 3.8+ | Core programming language |
| **AI Model** | Llama 3.1-8B-Instant | Latest | Text generation |
| **API Provider** | Groq | Latest | LLM inference service |

### 6.2 Supporting Libraries

| Library | Purpose |
|---------|---------|
| `requests` | HTTP client for API communication |
| `pydantic` | Data validation and parsing |
| `uvicorn` | ASGI server for FastAPI |
| `python-dotenv` | Environment variable management |
| `json` | Data serialization |
| `re` | Regular expressions for text processing |
| `statistics` | Statistical calculations |
| `collections.Counter` | Frequency counting |
| `datetime` | Timestamp generation |

### 6.3 Development Tools

- **Version Control**: Git
- **Code Editor**: VS Code
- **Package Manager**: pip
- **Virtual Environment**: venv
- **API Testing**: Postman/Thunder Client
- **Documentation**: Markdown

---

## 7. INTERFACE SPECIFICATIONS

### 7.1 User Interface (Frontend)

**Input Elements**:
1. **Prompt Text Area**
   - Multi-line input
   - Placeholder text
   - Minimum height: 120px
   - Neon green border with glow

2. **Domain Text Input**
   - Single-line input
   - Examples: technology, education, finance
   - Optional field

3. **Word Count Slider**
   - Range: 750 to 2000 words
   - Default: 750 words
   - Step: 50 words
   - Gradient track (green to pink)

**Output Elements**:
1. **Generated Content Display**
   - Read-only text area
   - Scrollable
   - Copy-paste enabled

2. **Metrics Panel**
   - Expandable section
   - Key metrics displayed
   - Formatted with labels and values

3. **Download Button**
   - Generates .txt file
   - Filename: `generated_content.txt`
   - Cyberpunk styling

**Visual Design**:
- **Background**: Radial gradient (#0f2027 → #2c5364 → #181818)
- **Primary Color**: Neon green (#39ff14)
- **Accent Color**: Neon pink (#ff00cc)
- **Font**: Orbitron, Share Tech Mono, Inter
- **Effects**: Glowing borders, box shadows, hover animations

### 7.2 API Interface (Backend)

**Endpoint**: `POST /generate`

**Request Schema**:
```python
{
  "prompt": str,        # Required: User's content prompt
  "max_words": int,     # Required: Desired word count (100-2000)
  "domain": str         # Required: Content domain
}
```

**Response Schema**:
```python
{
  "text": str,                  # Generated article content
  "keywords": List[str],        # Extracted keywords
  "dmk_ok": bool,              # Keyword validation status
  "quality_metrics": {
    "total_keywords": int,
    "present_keywords": int,
    "keyword_density": float,
    "well_distributed": int,
    "context_quality": int,
    "detailed_analysis": Dict
  }
}
```

**Error Response**:
```python
{
  "detail": str  # Error message
}
```

**Status Codes**:
- `200 OK`: Successful generation
- `400 Bad Request`: Invalid input
- `500 Internal Server Error`: Generation failure

### 7.3 External API Interface (Groq)

**Endpoint**: `https://api.groq.com/openai/v1/chat/completions`

**Authentication**: Bearer token (API key)

**Request Format**:
```python
{
  "model": "llama-3.1-8b-instant",
  "messages": [
    {
      "role": "system",
      "content": "System prompt with instructions"
    },
    {
      "role": "user",
      "content": "Enhanced prompt with keywords"
    }
  ],
  "max_tokens": int,        # Calculated dynamically
  "temperature": 0.7,       # Creativity control
  "top_p": 0.9,            # Nucleus sampling
  "stop": null             # No stop sequences
}
```

---

## 8. SECURITY CONSIDERATIONS

### 8.1 API Key Management
- Groq API key stored in `.env` file
- Environment variables loaded via `python-dotenv`
- Never commit `.env` to version control
- Key rotation policy recommended

### 8.2 Input Validation
- Frontend validates input completeness
- Backend validates with Pydantic schemas
- Sanitization of user inputs
- Length limits on text inputs

### 8.3 Data Privacy
- No user data stored long-term
- JSON logs contain only generated content metrics
- No personally identifiable information collected
- HTTPS for all API communications

### 8.4 Error Handling
- Graceful degradation on API failures
- User-friendly error messages
- Detailed logging for debugging
- No sensitive information in error messages

---

## 9. PERFORMANCE CONSIDERATIONS

### 9.1 Response Time Optimization
- **Achieved**: 4.46 seconds average
- **Strategies**:
  - Efficient keyword extraction (< 0.1s)
  - Groq API's high-speed inference
  - Minimal post-processing overhead

### 9.2 Scalability
- **Concurrent Users**: Designed for 10+ simultaneous requests
- **Stateless Design**: Each request independent
- **API Rate Limits**: Managed by Groq
- **Resource Usage**: Low memory footprint

### 9.3 Caching Strategies
- No caching currently implemented
- Future: Cache common prompt patterns
- Future: Memoize keyword extraction results

### 9.4 Token Optimization
- Dynamic token calculation based on word count
- 30% buffer prevents cut-offs while minimizing excess
- Average 120-125% word count accuracy

---

## 10. ERROR HANDLING AND RECOVERY

### 10.1 Frontend Error Handling
- Network errors: Display user-friendly message
- Timeout errors: Suggest retry
- Validation errors: Highlight missing fields
- Display errors in status area

### 10.2 Backend Error Handling
- API communication failures: Return 500 with details
- Validation failures: Return 400 with specific errors
- Timeout handling: Configurable timeout limits
- Logging all errors for debugging

### 10.3 Groq API Error Handling
- Rate limit exceeded: Inform user, suggest retry
- Invalid API key: Log error, prevent further requests
- Model unavailable: Graceful failure message
- Network errors: Retry logic (future enhancement)

---

## 11. DEPLOYMENT ARCHITECTURE

### 11.1 Local Development
```
Developer Machine
├── Frontend: localhost:8501 (Streamlit)
├── Backend: localhost:8000 (FastAPI)
└── External: Groq API (HTTPS)
```

### 11.3 Deployment Steps
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment: Create `.env` with API key
3. Start backend: `uvicorn llama_api:app --reload --port 8000`
4. Start frontend: `streamlit run longform_streamlit.py`
5. Access at: `http://localhost:8501`

---

## 12. MONITORING AND LOGGING

### 12.1 Application Logging
- Backend logs requests and responses
- Error tracking with stack traces
- Performance metrics logged
- Log level: INFO for production

### 12.2 Metrics Collection
- All generations logged to `generation_logs.json`
- Aggregate metrics in `final_metrics_report.json`
- Real-time metrics displayed to users
- Historical analysis available

### 12.3 Performance Monitoring
- Response time tracking
- Keyword accuracy trends
- Word count precision monitoring
- Success/failure rates

---

## 13. FUTURE ENHANCEMENTS

### 13.1 Architectural Improvements
- Database integration (PostgreSQL/MongoDB)
- Redis caching for common prompts
- Microservices architecture for scalability
- WebSocket for real-time updates

### 13.2 Feature Additions
- User authentication and accounts
- Generation history per user
- Custom keyword lists
- Multiple output formats (PDF, HTML, Markdown)
- A/B testing for prompts

### 13.3 Performance Optimizations
- Asynchronous processing
- Request queuing system
- Result caching
- CDN for static assets

---

## 14. GLOSSARY

- **DCKG**: Domain-Constrained Keyword Generation - Algorithm for extracting relevant keywords
- **DMK**: Domain-aware Model for Keyword enforcement - Algorithm for ensuring keyword presence
- **Llama 3.1**: Meta's large language model, 8B parameter variant
- **Groq**: AI inference API provider offering high-speed LLM processing
- **FastAPI**: Modern Python web framework for building APIs
- **Streamlit**: Python framework for building data and ML web applications
- **Unigram**: Single word token
- **Bigram**: Two-word phrase
- **TF-IDF**: Term Frequency-Inverse Document Frequency
- **Token**: Basic unit of text processing in language models

---
