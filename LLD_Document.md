# Low-Level Design (LLD) Document
## Freeform Text Generation for Content Creators

### 1. DOCUMENT INFORMATION

**Project Name:** Freeform Text Generation for Content Creators  
**Document Type:** Low-Level Design  
**Version:** 1.0  
**Date:** August 30, 2025  

### 2. INTRODUCTION

#### 2.1 Purpose
This document provides detailed technical specifications, class structures, method implementations, and algorithmic details for the Freeform Text Generation system.

#### 2.2 Scope
- Detailed module specifications
- Class and method definitions
- API endpoint specifications
- Database schemas (if applicable)
- Algorithm implementations

### 3. SYSTEM MODULES DETAILED DESIGN

#### 3.1 Frontend Module (longform_streamlit.py)

##### 3.1.1 Module Overview
```python
# File: longform_streamlit.py
# Purpose: Streamlit-based user interface
# Dependencies: streamlit, requests, time
```

##### 3.1.2 Key Components

**Configuration Setup:**
```python
st.set_page_config(
    page_title="Freeform Text Generation for Content Creators",
    layout="wide",
    initial_sidebar_state="auto"
)
```

**CSS Styling Class:**
```css
/* Cyberpunk Theme Variables */
--primary-bg: radial-gradient(ellipse at top left, #0f2027 0%, #2c5364 60%, #181818 100%)
--neon-green: #39ff14
--neon-pink: #ff00cc
--dark-gradient: linear-gradient(90deg, #0f2027 0%, #23272f 100%)
--font-family: 'Orbitron', 'Share Tech Mono', 'Inter', sans-serif
```

**Input Components:**
```python
# Text Area Component
prompt = st.text_area(
    label="Enter your prompt for longform text:",
    height=180,
    key="prompt_input"
)

# Text Input Component
domain = st.text_input(
    label="Enter domain (e.g. education, marketing, technology, etc.):",
    key="domain_input"
)

# Slider Component
word_count = st.slider(
    label="Desired word count:",
    min_value=750,
    max_value=2000,
    value=750,
    step=50,
    key="word_count_slider"
)
```

**API Communication Method:**
```python
def make_api_request(prompt: str, domain: str, word_count: int) -> dict:
    """
    Sends request to FastAPI backend
    
    Args:
        prompt (str): User input prompt
        domain (str): Content domain
        word_count (int): Desired word count
        
    Returns:
        dict: API response containing generated text
        
    Raises:
        requests.RequestException: If API call fails
    """
    API_URL = "http://localhost:8000/generate"
    
    payload = {
        "prompt": prompt,
        "max_words": word_count,
        "domain": domain
    }
    
    response = requests.post(API_URL, json=payload)
    return response
```

##### 3.1.3 Event Handlers

**Generate Button Handler:**
```python
if st.button("Generate", help="Generate longform text using your context and domain"):
    time.sleep(1)  # UX delay
    
    # Input validation
    if not prompt.strip():
        st.warning("Please enter a prompt.")
        return
    
    # API call with spinner
    with st.spinner("Generating text..."):
        try:
            response = make_api_request(prompt, domain, word_count)
            handle_api_response(response)
        except Exception as e:
            st.error(f"Error connecting to Llama API: {e}")
```

#### 3.2 Backend API Module (llama_api.py)

##### 3.2.1 Module Structure

**Imports and Configuration:**
```python
import os
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import logging

# Environment setup
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

**Pydantic Models:**
```python
class GenerateRequest(BaseModel):
    """
    Request model for text generation endpoint
    
    Attributes:
        prompt (str): User input prompt
        max_words (int): Maximum word count, default 800
        domain (str): Content domain specification
    """
    prompt: str
    max_words: int = 800
    domain: str
    
    class Config:
        schema_extra = {
            "example": {
                "prompt": "Write about space exploration",
                "max_words": 1000,
                "domain": "technology"
            }
        }

class GenerateResponse(BaseModel):
    """
    Response model for text generation
    
    Attributes:
        text (str): Generated content
        keywords (list): Extracted keywords
        dmk_ok (bool): DMK validation status
        missing_keywords (list, optional): Missing keywords if DMK fails
        warning (str, optional): Warning message if applicable
    """
    text: str
    keywords: list
    dmk_ok: bool
    missing_keywords: list = []
    warning: str = ""
```

##### 3.2.2 Core API Endpoint

**Generate Endpoint Implementation:**
```python
@app.post("/generate", response_model=GenerateResponse)
async def generate(data: GenerateRequest = Body(...)):
    """
    Main text generation endpoint
    
    Args:
        data (GenerateRequest): Request containing prompt, word count, and domain
        
    Returns:
        JSONResponse: Generated text with metadata
        
    Process Flow:
        1. Extract keywords using DCKG
        2. Apply DMK loss for keyword enforcement
        3. Call Groq API with enhanced prompt
        4. Validate response completeness
        5. Perform post-generation DMK validation
        6. Return formatted response
    """
    
    # Step 1: DCKG - Generate keywords
    keywords = generate_keywords(data.prompt, data.domain)
    logger.info(f"Generated keywords: {keywords}")
    
    # Step 2: DMK - Apply keyword constraints
    prompt_with_keywords = apply_dmk_loss(data.prompt, keywords)
    logger.info(f"Prompt after DMK: {prompt_with_keywords}")
    
    # Step 3: Groq API call
    groq_response = await call_groq_api(prompt_with_keywords, data.max_words)
    
    # Step 4: Response processing
    if groq_response.status_code == 200:
        text = extract_and_clean_text(groq_response.json())
        
        # Step 5: Post-generation validation
        dmk_ok, missing_keywords = apply_dmk_loss(
            data.prompt, keywords, generated_text=text
        )
        
        return create_response(text, keywords, dmk_ok, missing_keywords)
    else:
        logger.error(f"Groq API error: {groq_response.text}")
        return JSONResponse(
            content={"error": groq_response.text}, 
            status_code=500
        )
```

##### 3.2.3 Helper Methods

**Groq API Integration:**
```python
async def call_groq_api(prompt: str, max_words: int) -> requests.Response:
    """
    Calls Groq API for text generation
    
    Args:
        prompt (str): Enhanced prompt with keywords
        max_words (int): Maximum word count
        
    Returns:
        requests.Response: API response object
    """
    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system", 
                "content": "You are a professional content writer. Always complete your sentences and paragraphs. Never end abruptly or leave sentences unfinished. Ensure your response is complete and well-structured."
            },
            {"role": "user", "content": prompt}
        ],
        "max_tokens": int(max_words * 1.8),
        "temperature": 0.7,
        "top_p": 0.9,
        "stop": None
    }
    
    return requests.post(groq_url, headers=headers, json=payload)
```

**Text Processing:**
```python
def extract_and_clean_text(api_response: dict) -> str:
    """
    Extracts and cleans text from Groq API response
    
    Args:
        api_response (dict): JSON response from Groq API
        
    Returns:
        str: Cleaned and validated text
        
    Processing Steps:
        1. Extract content from response
        2. Strip whitespace
        3. Remove incomplete sentences
        4. Ensure proper ending
    """
    text = api_response["choices"][0]["message"]["content"]
    text = text.strip()
    
    # Remove incomplete sentences at the end
    sentences = text.split('.')
    if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
        text = '.'.join(sentences[:-1]) + '.'
    
    return text
```

#### 3.3 DCKG Module (dckg.py)

##### 3.3.1 Module Overview
```python
# File: dckg.py
# Purpose: Domain-Constrained Knowledge Generation
# Algorithm: Frequency-based keyword extraction with stopword filtering
```

##### 3.3.2 Core Algorithm

**Keyword Generation Function:**
```python
def generate_keywords(prompt: str, domain: str, top_n: int = 10) -> list:
    """
    Lightweight keyword extraction using word frequency and stopwords
    
    Args:
        prompt (str): Input text for keyword extraction
        domain (str): Domain context (currently used for future enhancement)
        top_n (int): Number of top keywords to return, default 10
        
    Returns:
        list: List of extracted keywords sorted by frequency
        
    Algorithm:
        1. Define stopwords set
        2. Tokenize prompt using regex
        3. Filter words by length and stopword status
        4. Count word frequencies
        5. Return top_n most frequent keywords
        
    Time Complexity: O(n log n) where n is number of words
    Space Complexity: O(n) for word storage
    """
    
    # Step 1: Stopwords definition
    stopwords = set([
        "the", "is", "in", "and", "to", "of", "a", "for", "on", "with",
        "as", "by", "an", "be", "are", "at", "from", "that", "this",
        "it", "or", "was", "but", "not", "can", "has", "have", "will",
        "which", "their", "more", "than", "about", "into", "also",
        "such", "other", "use", "used", "using", "these", "may",
        "been", "were", "should", "could", "would", "our", "your",
        "his", "her", "its", "they", "them", "he", "she", "we", "you", "i"
    ])
    
    # Step 2: Tokenization
    words = re.findall(r'\w+', prompt.lower())
    
    # Step 3: Filtering
    keywords = [
        word for word in words 
        if word not in stopwords and len(word) > 3
    ]
    
    # Step 4: Frequency counting
    freq = Counter(keywords)
    
    # Step 5: Return top keywords
    return [word for word, _ in freq.most_common(top_n)]
```

##### 3.3.3 Data Structures

**Stopwords Set:**
```python
STOPWORDS = {
    # Common English stopwords
    "the", "is", "in", "and", "to", "of", "a", "for", "on", "with",
    # ... (complete list as shown in implementation)
}
```

**Frequency Counter:**
```python
from collections import Counter

# Usage in keyword extraction
freq_counter = Counter(filtered_keywords)
top_keywords = freq_counter.most_common(top_n)
```

#### 3.4 DMK Module (dmk.py)

##### 3.4.1 Module Overview
```python
# File: dmk.py
# Purpose: Domain-Constrained Model Knowledge enforcement
# Functionality: Pre and post-generation keyword validation
```

##### 3.4.2 Core Implementation

**DMK Loss Application:**
```python
def apply_dmk_loss(prompt: str, keywords: list, generated_text: str = None) -> Union[str, Tuple[bool, list]]:
    """
    Simulate traditional DMK loss enforcement
    
    Args:
        prompt (str): Original user prompt
        keywords (list): List of keywords to enforce
        generated_text (str, optional): Generated text for validation
        
    Returns:
        Union[str, Tuple[bool, list]]: 
            - If generated_text is None: Enhanced prompt string
            - If generated_text provided: (validation_result, missing_keywords)
            
    Modes:
        1. Pre-generation: Enhance prompt with keyword instructions
        2. Post-generation: Validate keyword presence in generated text
    """
    
    # Early return for empty keywords
    if not keywords:
        return prompt if generated_text is None else (True, [])
    
    # Post-generation validation mode
    if generated_text is not None:
        missing = [
            keyword for keyword in keywords 
            if keyword.lower() not in generated_text.lower()
        ]
        
        if missing:
            return False, missing  # DMK constraint not satisfied
        return True, []  # All keywords present
    
    # Pre-generation enhancement mode
    instruction = create_enhanced_prompt(prompt, keywords)
    return instruction

def create_enhanced_prompt(prompt: str, keywords: list) -> str:
    """
    Creates enhanced prompt with keyword instructions
    
    Args:
        prompt (str): Original prompt
        keywords (list): Keywords to incorporate
        
    Returns:
        str: Enhanced prompt with keyword constraints
    """
    min_words = len(keywords) * 100 + 750
    
    instruction = (
        f"Write a comprehensive, well-structured long-form article "
        f"(minimum {min_words} words) that naturally incorporates "
        f"all of these important keywords: {', '.join(keywords)}. "
        f"Ensure the article is complete with a proper conclusion. "
        f"Do not end abruptly or leave sentences unfinished. "
        f"The keywords should be woven seamlessly into the content, "
        f"not just listed. Context: {prompt}"
    )
    
    return instruction
```

##### 3.4.3 Validation Algorithms

**Keyword Presence Check:**
```python
def validate_keyword_presence(text: str, keywords: list) -> Tuple[bool, list]:
    """
    Validates presence of keywords in generated text
    
    Args:
        text (str): Generated text to validate
        keywords (list): Keywords to check for
        
    Returns:
        Tuple[bool, list]: (all_present, missing_keywords)
        
    Algorithm:
        1. Convert text to lowercase for case-insensitive matching
        2. Check each keyword for presence in text
        3. Collect missing keywords
        4. Return validation result
        
    Time Complexity: O(k * n) where k is keywords count, n is text length
    Space Complexity: O(k) for missing keywords list
    """
    text_lower = text.lower()
    missing_keywords = []
    
    for keyword in keywords:
        if keyword.lower() not in text_lower:
            missing_keywords.append(keyword)
    
    all_present = len(missing_keywords) == 0
    return all_present, missing_keywords
```

### 4. API SPECIFICATIONS

#### 4.1 REST API Endpoints

**Base URL:** `http://localhost:8000`

##### 4.1.1 Generate Text Endpoint

**Endpoint:** `POST /generate`

**Request Schema:**
```json
{
    "prompt": "string (required)",
    "max_words": "integer (optional, default: 800)",
    "domain": "string (required)"
}
```

**Response Schema:**
```json
{
    "text": "string",
    "keywords": ["string"],
    "dmk_ok": "boolean",
    "missing_keywords": ["string"],
    "warning": "string"
}
```

**Error Responses:**
```json
// 500 Internal Server Error
{
    "error": "string"
}

// 422 Validation Error
{
    "detail": [
        {
            "loc": ["string"],
            "msg": "string",
            "type": "string"
        }
    ]
}
```

### 5. DATA STRUCTURES

#### 5.1 Internal Data Models

**Keyword Frequency Structure:**
```python
keyword_freq = {
    "keyword1": 5,
    "keyword2": 3,
    "keyword3": 2
}
```

**API Response Structure:**
```python
api_response = {
    "choices": [
        {
            "message": {
                "content": "Generated text content..."
            }
        }
    ]
}
```

**DMK Validation Result:**
```python
dmk_result = {
    "is_valid": True,
    "missing_keywords": [],
    "validation_score": 1.0
}
```

### 6. ALGORITHMS AND COMPLEXITY

#### 6.1 Keyword Extraction Algorithm

**Time Complexity Analysis:**
- Tokenization: O(n) where n is prompt length
- Filtering: O(w) where w is word count
- Frequency counting: O(w)
- Sorting: O(w log w)
- **Overall: O(w log w)**

**Space Complexity Analysis:**
- Word storage: O(w)
- Frequency counter: O(u) where u is unique words
- **Overall: O(w)**

#### 6.2 DMK Validation Algorithm

**Time Complexity Analysis:**
- Keyword checking: O(k * t) where k is keyword count, t is text length
- Missing keyword collection: O(k)
- **Overall: O(k * t)**

**Space Complexity Analysis:**
- Missing keywords list: O(k)
- **Overall: O(k)**

### 7. ERROR HANDLING

#### 7.1 Exception Hierarchy

```python
class APIError(Exception):
    """Base exception for API errors"""
    pass

class GroqAPIError(APIError):
    """Groq API specific errors"""
    pass

class ValidationError(APIError):
    """Input validation errors"""
    pass

class DMKValidationError(APIError):
    """DMK constraint validation errors"""
    pass
```

#### 7.2 Error Handling Strategies

**API Level Error Handling:**
```python
try:
    response = requests.post(groq_url, headers=headers, json=payload)
    response.raise_for_status()
except requests.RequestException as e:
    logger.error(f"Groq API call failed: {e}")
    raise GroqAPIError(f"External API error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise APIError(f"Internal server error: {e}")
```

**Frontend Error Handling:**
```python
try:
    response = make_api_request(prompt, domain, word_count)
    if response.status_code == 200:
        display_success(response.json())
    else:
        st.error(f"API Error: {response.status_code} - {response.text}")
except requests.ConnectionError:
    st.error("Unable to connect to the API. Please check if the server is running.")
except Exception as e:
    st.error(f"Unexpected error: {e}")
```

### 8. PERFORMANCE OPTIMIZATION

#### 8.1 Caching Strategies

**Keyword Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def generate_keywords_cached(prompt: str, domain: str) -> tuple:
    """Cached version of keyword generation"""
    return tuple(generate_keywords(prompt, domain))
```

**Response Caching:**
```python
# Future implementation for frequently requested content
response_cache = {
    "prompt_hash": {
        "text": "cached_response",
        "timestamp": "cache_time",
        "expiry": "cache_expiry"
    }
}
```

#### 8.2 Optimization Techniques

**Async Processing:**
```python
import asyncio

async def process_multiple_requests(requests: list) -> list:
    """Process multiple generation requests concurrently"""
    tasks = [generate_text_async(req) for req in requests]
    return await asyncio.gather(*tasks)
```

### 9. TESTING SPECIFICATIONS

#### 9.1 Unit Test Cases

**DCKG Module Tests:**
```python
def test_keyword_extraction():
    prompt = "Space exploration is fascinating and revolutionary"
    keywords = generate_keywords(prompt, "technology")
    assert "space" in keywords
    assert "exploration" in keywords
    assert len(keywords) <= 10

def test_empty_prompt():
    keywords = generate_keywords("", "technology")
    assert keywords == []
```

**DMK Module Tests:**
```python
def test_dmk_validation_success():
    keywords = ["space", "exploration"]
    text = "Space exploration is the future of humanity"
    result, missing = apply_dmk_loss("", keywords, text)
    assert result is True
    assert missing == []

def test_dmk_validation_failure():
    keywords = ["artificial", "intelligence"]
    text = "Space exploration is exciting"
    result, missing = apply_dmk_loss("", keywords, text)
    assert result is False
    assert "artificial" in missing
    assert "intelligence" in missing
```

#### 9.2 Integration Test Cases

**API Endpoint Tests:**
```python
def test_generate_endpoint():
    request_data = {
        "prompt": "Write about space exploration",
        "max_words": 1000,
        "domain": "technology"
    }
    response = client.post("/generate", json=request_data)
    assert response.status_code == 200
    assert "text" in response.json()
    assert "keywords" in response.json()
```

### 10. DEPLOYMENT SPECIFICATIONS

#### 10.1 Environment Configuration

**Development Environment:**
```bash
# .env file structure
GROQ_API_KEY=your_api_key_here
ENVIRONMENT=development
LOG_LEVEL=DEBUG
API_HOST=localhost
API_PORT=8000
STREAMLIT_PORT=8501
```

**Production Environment:**
```bash
# Production configuration
GROQ_API_KEY=production_api_key
ENVIRONMENT=production
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
```

#### 10.2 Startup Scripts

**FastAPI Startup:**
```bash
#!/bin/bash
# start_api.sh
source venv/bin/activate
uvicorn llama_api:app --host 0.0.0.0 --port 8000 --reload
```

**Streamlit Startup:**
```bash
#!/bin/bash
# start_frontend.sh
source venv/bin/activate
streamlit run longform_streamlit.py --server.port 8501
```

### 11. CONCLUSION

This Low-Level Design document provides comprehensive technical specifications for implementing the Freeform Text Generation system. The modular architecture ensures maintainability, scalability, and testability while delivering high-performance content generation capabilities.

