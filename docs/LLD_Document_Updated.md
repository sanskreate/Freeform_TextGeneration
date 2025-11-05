# Low-Level Design (LLD) Document
## Freeform Text Generation for Content Creators

### DOCUMENT INFORMATION

**Project Name:** Freeform Text Generation for Content Creators  
**Document Type:** Low-Level Design  
**Version:** 2.0  
**Date:** November 6, 2025  
**Author:** Sanskriti Rai  
**Organization:** PW Skills (Physics Wallah Pvt. Ltd.)  
**Mentor:** Mr. Sudhanshu

---

## 1. INTRODUCTION

### 1.1 Purpose
This Low-Level Design document provides detailed technical specifications for all modules, classes, functions, algorithms, and data structures used in the Freeform Text Generation system. It serves as a comprehensive guide for implementation, testing, and maintenance.

### 1.2 Scope
- Detailed module specifications with complete code structure
- Function signatures and implementations
- Algorithm pseudocode and flowcharts
- Data models and schemas
- Database structures (JSON storage)
- Error handling strategies
- Performance optimization techniques

### 1.3 Intended Audience
- Software developers implementing the system
- Quality assurance engineers writing test cases
- Code reviewers evaluating implementation
- Future maintainers and enhancers

---

## 2. MODULE DESIGN

### 2.1 Frontend Module: longform_streamlit.py

#### 2.1.1 Module Overview
- **File**: `longform_streamlit.py`
- **Framework**: Streamlit 1.30.0+
- **Purpose**: Provide cyberpunk-themed web interface for content generation
- **Dependencies**: streamlit, requests, time, json, os, test_results

#### 2.1.2 Configuration Setup

```python
import streamlit as st
import time
import requests
import json
import os
from test_results import analyze_generation, log_generation

# Page Configuration
st.set_page_config(
    page_title="Freeform Text Generation for Content Creators",
    layout="wide",
    initial_sidebar_state="auto"
)
```

**Purpose**: Initialize Streamlit application with custom page settings

#### 2.1.3 CSS Styling

```python
st.markdown("""
<style>
    /* Global Styles */
    body, .stApp {
        background: radial-gradient(ellipse at top left, #0f2027 0%, #2c5364 60%, #181818 100%);
        color: #e0e0e0;
        font-family: 'Orbitron', 'Share Tech Mono', 'Inter', sans-serif;
        letter-spacing: 1.2px;
    }
    
    /* Input Field Styles */
    .stTextInput>div>div>input, .stTextArea textarea {
        font-size: 1.22rem;
        background: linear-gradient(90deg, #23272f 0%, #0f2027 100%);
        color: #39ff14;
        border-radius: 12px;
        border: 1.5px solid #39ff14;
        padding: 1em 1.2em;
        box-shadow: 0 0 12px #39ff1444, 0 0 2px #ff00cc44;
        text-shadow: 0 0 2px #39ff14, 0 0 8px #ff00cc;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(90deg, #0f2027 0%, #ff00cc 100%) !important;
        color: #39ff14 !important;
        font-size: 1.18rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 0.9em 2.5em !important;
        border: 2px solid #39ff14 !important;
        box-shadow: 0 0 16px #ff00cc88, 0 0 8px #39ff1444 !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #ff00cc 0%, #39ff14 100%) !important;
        box-shadow: 0 0 32px #ff00cc, 0 0 16px #39ff14 !important;
    }
</style>
""", unsafe_allow_html=True)
```

**CSS Variables**:
- `--bg-gradient`: Radial gradient from #0f2027 to #181818
- `--neon-green`: #39ff14
- `--neon-pink`: #ff00cc
- `--dark-bg`: #23272f

#### 2.1.4 User Input Components

```python
# Header
st.markdown(
    "<h1 style='text-align:center; font-size:3.5rem; color:#39ff14; "
    "text-shadow: 0 0 15px #39ff14, 0 0 40px #ff00cc;'>"
    "🌐 NEURAL TEXT SYNTHESIZER 🌐</h1>",
    unsafe_allow_html=True
)

# Prompt Input
prompt = st.text_area(
    label="📝 Content Prompt",
    placeholder="Enter your content idea or topic...",
    height=150,
    key="prompt_input"
)

# Domain Input
domain = st.text_input(
    label="🎯 Domain",
    placeholder="e.g. technology, education, finance, health",
    key="domain_input"
)

# Word Count Slider
word_count = st.slider(
    label="📏 Desired Word Count",
    min_value=100,
    max_value=2000,
    value=750,
    step=50,
    key="word_count_slider"
)
```

**Input Validation**:
- Prompt: Required, minimum 10 characters
- Domain: Optional, alphanumeric only
- Word Count: Integer between 100-2000

#### 2.1.5 API Communication Function

```python
def make_api_request(prompt: str, domain: str, word_count: int) -> dict:
    """
    Send generation request to FastAPI backend
    
    Args:
        prompt: User's content prompt
        domain: Content domain
        word_count: Desired word count
        
    Returns:
        dict: Response from API containing generated text and metrics
        
    Raises:
        requests.exceptions.RequestException: On API communication failure
    """
    api_url = "http://127.0.0.1:8000/generate"
    
    payload = {
        "prompt": prompt,
        "max_words": word_count,
        "domain": domain
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            api_url,
            json=payload,
            headers=headers,
            timeout=60  # 60 second timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise Exception("Request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        raise Exception("Cannot connect to backend API. Ensure it's running.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"API error: {e.response.text}")
```

#### 2.1.6 Generation Handler

```python
if st.button("⚡ Generate", help="Generate longform text"):
    if not prompt:
        st.error("❌ Please enter a prompt")
    elif not domain:
        st.error("❌ Please specify a domain")
    else:
        with st.spinner("🔄 Generating content..."):
            try:
                # Start timer
                start_time = time.time()
                
                # Call API
                response = make_api_request(prompt, domain, word_count)
                
                # Calculate response time
                response_time = time.time() - start_time
                
                # Extract response data
                generated_text = response.get("text", "")
                keywords = response.get("keywords", [])
                quality_metrics = response.get("quality_metrics", {})
                
                # Analyze generation
                metrics = analyze_generation(
                    prompt=prompt,
                    generated_text=generated_text,
                    response_time_s=response_time,
                    requested_words=word_count
                )
                
                # Log results
                log_generation(metrics)
                
                # Display success
                st.success("✅ Content generated successfully!")
                
                # Display generated content
                st.text_area(
                    label="📄 Generated Content",
                    value=generated_text,
                    height=400,
                    key="output_text"
                )
                
                # Display metrics in expander
                with st.expander("📊 Performance Metrics", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Response Time", f"{response_time:.2f}s")
                        st.metric("Keyword Accuracy", 
                                 f"{metrics['keyword_accuracy%']}%")
                        st.metric("Word Count", 
                                 f"{metrics['length_metrics']['actual']} words")
                    
                    with col2:
                        st.metric("Keyword Enforcement", 
                                 f"{metrics['keyword_enforcement%']}%")
                        st.metric("Word Count Accuracy", 
                                 f"{metrics['length_metrics']['accuracy%']}%")
                        st.metric("Unique Words", 
                                 f"{metrics['length_metrics']['unique%']}%")
                    
                    # Display keywords
                    st.write("**Extracted Keywords:**")
                    st.write(", ".join(keywords))
                
                # Download button
                st.download_button(
                    label="💾 Download Content",
                    data=generated_text,
                    file_name="generated_content.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
```

**Event Flow**:
1. Validate inputs
2. Start timer
3. Send API request
4. Receive response
5. Calculate metrics
6. Log to JSON
7. Display results
8. Provide download option

---

### 2.2 Backend Module: llama_api.py

#### 2.2.1 Module Overview
- **File**: `llama_api.py`
- **Framework**: FastAPI
- **Purpose**: Handle API requests and orchestrate content generation
- **Dependencies**: fastapi, pydantic, requests, dotenv, logging, dckg, dmk

#### 2.2.2 Imports and Configuration

```python
import os
import logging
import requests
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from dckg import generate_keywords
from dmk import apply_dmk_loss

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

#### 2.2.3 Data Models

```python
class GenerateRequest(BaseModel):
    """
    Request model for content generation
    
    Attributes:
        prompt (str): User's content prompt
        max_words (int): Desired word count (100-2000)
        domain (str): Content domain
    """
    prompt: str
    max_words: int = 800
    domain: str
    
    class Config:
        schema_extra = {
            "example": {
                "prompt": "Artificial intelligence is transforming healthcare",
                "max_words": 750,
                "domain": "technology"
            }
        }
```

#### 2.2.4 FastAPI Application

```python
app = FastAPI(
    title="Freeform Text Generation API",
    description="AI-powered long-form content generation with keyword enforcement",
    version="2.0.0"
)
```

#### 2.2.5 Main Generation Endpoint

```python
@app.post("/generate")
async def generate(data: GenerateRequest = Body(...)):
    """
    Generate long-form content with keyword enforcement
    
    Args:
        data: GenerateRequest object containing prompt, max_words, domain
        
    Returns:
        JSONResponse: Generated text, keywords, validation status, quality metrics
        
    Raises:
        500: On Groq API failure or internal error
    """
    
    # Extract request data
    prompt = data.prompt
    max_words = data.max_words
    domain = data.domain
    
    logger.info(f"Received generation request: domain={domain}, words={max_words}")
    
    # STEP 1: Generate keywords using DCKG
    keywords = generate_keywords(prompt, domain, top_n=10)
    logger.info(f"DCKG extracted keywords: {keywords}")
    
    # STEP 2: Enhance prompt with DMK
    prompt_with_keywords = apply_dmk_loss(prompt, keywords)
    logger.info(f"DMK enhanced prompt created")
    
    # STEP 3: Configure Groq API request
    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # STEP 4: Calculate max_tokens with buffer
    # Formula: (words / 0.75 words_per_token) * 1.3 buffer
    target_tokens = int((max_words / 0.75) * 1.3)
    logger.info(f"Calculated target_tokens: {target_tokens}")
    
    # STEP 5: Build request payload
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional content writer. "
                    "Write comprehensive, well-structured content. "
                    "Always complete your sentences and paragraphs fully. "
                    "Never end abruptly or leave sentences unfinished. "
                    "Aim for the requested word count but prioritize "
                    "completing your thoughts."
                )
            },
            {
                "role": "user",
                "content": prompt_with_keywords
            }
        ],
        "max_tokens": target_tokens,
        "temperature": 0.7,  # Balanced creativity
        "top_p": 0.9,        # Nucleus sampling
        "stop": None         # No stop sequences
    }
    
    # STEP 6: Send request to Groq API
    try:
        response = requests.post(groq_url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Groq API error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"API communication failed: {str(e)}"}
        )
    
    # STEP 7: Extract generated text
    result = response.json()
    text = result["choices"][0]["message"]["content"]
    
    # STEP 8: Clean up text
    text = text.strip()
    
    # Remove incomplete sentences at the end
    sentences = text.split('.')
    if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
        # Last sentence is too short (likely incomplete)
        text = '.'.join(sentences[:-1]) + '.'
    
    logger.info(f"Text generated successfully. Length: {len(text.split())} words")
    
    # STEP 9: Validate with DMK post-generation
    dmk_ok, missing_keywords, quality_metrics = apply_dmk_loss(
        prompt, keywords, generated_text=text
    )
    
    if not dmk_ok:
        logger.warning(
            f"DMK validation warning. Missing keywords: {missing_keywords}"
        )
        logger.warning(f"Quality metrics: {quality_metrics}")
    
    logger.info(f"DMK validation complete. Success: {dmk_ok}")
    logger.info(f"Quality metrics: {quality_metrics}")
    
    # STEP 10: Return response
    return JSONResponse(content={
        "text": text,
        "keywords": keywords,
        "dmk_ok": dmk_ok,
        "quality_metrics": quality_metrics
    })
```

**Endpoint Specifications**:
- **URL**: `/generate`
- **Method**: POST
- **Content-Type**: application/json
- **Timeout**: 60 seconds
- **Rate Limiting**: Managed by Groq API

---

### 2.3 DCKG Module: dckg.py

#### 2.3.1 Module Overview
- **File**: `dckg.py`
- **Purpose**: Domain-agnostic keyword extraction
- **Algorithm**: Frequency-based scoring with contextual boosts
- **Dependencies**: re, collections.Counter, math

#### 2.3.2 Main Function

```python
import re
from collections import Counter
import math

def generate_keywords(prompt: str, domain: str, top_n: int = 10) -> list:
    """
    Domain-Constrained Keyword Generation (DCKG) Algorithm
    
    Extracts relevant keywords using domain-agnostic scoring that combines:
    - Term frequency (how often words appear)
    - Word length (longer = more specific)
    - Capitalization (proper nouns, important concepts)
    - Phrase detection (bigrams for multi-word expressions)
    
    Args:
        prompt (str): User's input text
        domain (str): Domain context (informational only)
        top_n (int): Number of keywords to return (default: 10)
        
    Returns:
        list: Top N keywords and phrases
        
    Algorithm Complexity:
        Time: O(n log n) where n = number of unique words
        Space: O(n) for frequency counters
    """
    
    # Define comprehensive stopword list
    stopwords = set([
        "the", "is", "in", "and", "to", "of", "a", "for", "on", "with",
        "as", "by", "an", "be", "are", "at", "from", "that", "this", "it",
        "or", "was", "but", "not", "can", "has", "have", "will", "which",
        "their", "more", "than", "about", "into", "also", "such", "other",
        "use", "used", "using", "these", "may", "been", "were", "should",
        "could", "would", "our", "your", "his", "her", "its", "they", "them",
        "he", "she", "we", "you", "i", "me", "my", "am", "who", "what",
        "where", "when", "why", "how", "all", "each", "every", "both", "few",
        "some", "any", "most", "no", "nor", "only", "own", "same", "so",
        "then", "very", "just", "now", "even", "well", "back", "through",
        "after", "before", "between", "under", "again", "further", "once",
        "here", "there", "during", "always", "whether", "however",
        "therefore", "thus", "hence", "write", "article", "comprehensive",
        "words", "content", "need", "make", "made", "get", "go", "come",
        "said", "say", "see", "know", "think", "take", "give", "find",
        "tell", "ask", "work", "seem", "feel", "try", "leave", "call"
    ])
    
    # STEP 1: Extract single words (unigrams)
    words = re.findall(r'\b[a-z]+\b', prompt.lower())
    
    # STEP 2: Extract two-word phrases (bigrams)
    bigrams = [
        f"{words[i]} {words[i+1]}"
        for i in range(len(words)-1)
        if words[i] not in stopwords 
        and words[i+1] not in stopwords
        and len(words[i]) > 3 
        and len(words[i+1]) > 3
    ]
    
    # STEP 3: Filter words
    filtered_words = [
        w for w in words 
        if w not in stopwords and len(w) > 3
    ]
    
    # STEP 4: Calculate frequencies
    word_freq = Counter(filtered_words)
    bigram_freq = Counter(bigrams)
    
    # STEP 5: Score keywords
    total_words = len(filtered_words)
    scored_keywords = {}
    
    # Score single words
    for word, freq in word_freq.items():
        # Base: Term Frequency
        tf_score = freq / total_words if total_words > 0 else 0
        
        # Boost 1: Length (longer words = more specific)
        # "sustainability" (14) > "green" (5)
        length_boost = 1 + (len(word) - 4) * 0.08 if len(word) > 4 else 1.0
        
        # Boost 2: Capitalization (proper nouns, important concepts)
        cap_pattern = r'\b' + word + r'\b'
        cap_boost = 1.4 if any(
            w[0].isupper() 
            for w in re.findall(cap_pattern, prompt, re.IGNORECASE)
        ) else 1.0
        
        # Boost 3: Frequency (repeated = more important)
        frequency_boost = 1 + (freq - 1) * 0.2 if freq > 1 else 1.0
        
        # Calculate final score
        final_score = tf_score * length_boost * cap_boost * frequency_boost
        scored_keywords[word] = final_score
    
    # Score bigrams (phrases)
    for bigram, freq in bigram_freq.items():
        # Phrases get strong bonus (more specific than single words)
        tf_score = (freq / total_words if total_words > 0 else 0) * 2.0
        
        # Boost if phrase contains high-frequency words
        words_in_phrase = bigram.split()
        contains_important = any(
            w in word_freq and word_freq[w] > 1 
            for w in words_in_phrase
        )
        importance_boost = 1.3 if contains_important else 1.0
        
        # Boost longer phrases
        phrase_length = len(bigram.replace(' ', ''))
        length_boost = 1 + (phrase_length - 10) * 0.03 if phrase_length > 10 else 1.0
        
        # Calculate final score
        final_score = tf_score * importance_boost * length_boost
        scored_keywords[bigram] = final_score
    
    # STEP 6: Sort and return top N
    sorted_keywords = sorted(
        scored_keywords.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return [kw for kw, score in sorted_keywords[:top_n]]
```

**Algorithm Pseudocode**:
```
DCKG(prompt, domain, top_n):
    1. Initialize stopwords set
    2. Extract words = tokenize(prompt)
    3. Extract bigrams = consecutive_word_pairs(words)
    4. Filter words by length > 3 and not in stopwords
    5. Calculate word_freq = count(filtered_words)
    6. Calculate bigram_freq = count(bigrams)
    7. For each word:
        a. Calculate TF score
        b. Apply length boost
        c. Apply capitalization boost
        d. Apply frequency boost
        e. Store final score
    8. For each bigram:
        a. Calculate TF score with phrase bonus
        b. Apply importance boost
        c. Apply length boost
        d. Store final score
    9. Sort all keywords by score descending
    10. Return top N keywords
```

---

### 2.4 DMK Module: dmk.py

#### 2.4.1 Module Overview
- **File**: `dmk.py`
- **Purpose**: Keyword enforcement through prompt enhancement and validation
- **Algorithm**: Two-phase approach (pre and post generation)
- **Dependencies**: re

#### 2.4.2 Main Function

```python
import re

def apply_dmk_loss(prompt: str, 
                   keywords: list, 
                   generated_text: str = None) -> tuple:
    """
    Domain-aware Model for Keyword enforcement (DMK) Algorithm
    
    Two-phase keyword enforcement:
    1. Pre-generation: Enhance prompt with keyword instructions
    2. Post-generation: Validate keyword presence and quality
    
    Args:
        prompt (str): Original user prompt
        keywords (list): Keywords to enforce
        generated_text (str, optional): Generated text for validation
        
    Returns:
        If generated_text is None:
            str: Enhanced prompt with keyword instructions
        If generated_text is provided:
            tuple: (success_bool, missing_keywords_list, quality_metrics_dict)
    """
    
    # Handle empty keywords
    if not keywords:
        return prompt if generated_text is None else (True, [], {})
    
    # ================== POST-GENERATION VALIDATION ==================
    if generated_text is not None:
        text_lower = generated_text.lower()
        text_length = len(generated_text.split())
        
        # Divide text into thirds for distribution analysis
        third_len = len(generated_text) // 3
        text_parts = [
            generated_text[:third_len].lower(),
            generated_text[third_len:2*third_len].lower(),
            generated_text[2*third_len:].lower()
        ]
        
        # Initialize metrics
        missing_keywords = []
        keyword_quality = {
            'total_keywords': len(keywords),
            'present_keywords': 0,
            'keyword_density': 0.0,
            'well_distributed': 0,
            'context_quality': 0,
            'detailed_analysis': {}
        }
        
        total_keyword_occurrences = 0
        
        # Analyze each keyword
        for kw in keywords:
            kw_lower = kw.lower()
            
            # Count occurrences (word boundary matching)
            if ' ' in kw:  # Multi-word phrase
                pattern = r'\b' + re.escape(kw_lower) + r'\b'
            else:  # Single word
                pattern = r'\b' + kw_lower + r'\b'
            
            occurrences = len(re.findall(pattern, text_lower))
            total_keyword_occurrences += occurrences
            
            # Check presence
            if occurrences == 0:
                missing_keywords.append(kw)
                keyword_quality['detailed_analysis'][kw] = {
                    'present': False,
                    'occurrences': 0,
                    'distribution': 'absent',
                    'context_quality': 'none'
                }
            else:
                keyword_quality['present_keywords'] += 1
                
                # Check distribution across sections
                parts_with_keyword = sum(
                    1 for part in text_parts 
                    if kw_lower in part
                )
                distribution = (
                    'excellent' if parts_with_keyword >= 2 
                    else 'clustered'
                )
                if parts_with_keyword >= 2:
                    keyword_quality['well_distributed'] += 1
                
                # Check context quality (in sentences, not lists)
                context_pattern = r'\w+\s+' + re.escape(kw_lower) + r'\s+\w+'
                in_context = len(re.findall(context_pattern, text_lower))
                context_qual = 'good' if in_context > 0 else 'poor'
                if in_context > 0:
                    keyword_quality['context_quality'] += 1
                
                keyword_quality['detailed_analysis'][kw] = {
                    'present': True,
                    'occurrences': occurrences,
                    'distribution': distribution,
                    'context_quality': context_qual
                }
        
        # Calculate keyword density
        if text_length > 0:
            keyword_quality['keyword_density'] = (
                total_keyword_occurrences / text_length
            ) * 100
        
        # Determine success
        # Criteria:
        # - Max 20% keywords missing
        # - At least 1% keyword density
        # - At least 50% keywords in good context
        presence_rate = (
            keyword_quality['present_keywords'] / len(keywords)
        ) * 100
        
        success = (
            len(missing_keywords) <= len(keywords) * 0.2 and
            keyword_quality['keyword_density'] >= 1.0 and
            keyword_quality['context_quality'] >= len(keywords) * 0.5
        )
        
        return success, missing_keywords, keyword_quality
    
    # ================== PRE-GENERATION ENHANCEMENT ==================
    
    # Categorize keywords
    single_keywords = [kw for kw in keywords if ' ' not in kw]
    phrase_keywords = [kw for kw in keywords if ' ' in kw]
    
    # Build enhanced prompt
    instruction_parts = []
    
    # Main instruction
    target_words = len(keywords) * 100 + 800
    instruction_parts.append(
        f"Write a comprehensive, well-structured long-form article "
        f"(approximately {target_words} words) on the following topic: {prompt}"
    )
    
    # Keyword requirements
    if single_keywords or phrase_keywords:
        instruction_parts.append("\n\nIMPORTANT KEYWORD REQUIREMENTS:")
        instruction_parts.append(
            "You MUST naturally incorporate the following keywords and phrases "
            "throughout the article. These should appear in meaningful context, "
            "distributed across different sections:"
        )
        
        if single_keywords:
            instruction_parts.append(
                f"\nKey Terms: {', '.join(single_keywords)}"
            )
        
        if phrase_keywords:
            instruction_parts.append(
                f"\nKey Phrases: {', '.join(phrase_keywords)}"
            )
        
        instruction_parts.append(
            "\n\nGUIDELINES FOR KEYWORD USAGE:"
            "\n- Use each keyword at least 2-3 times throughout the article"
            "\n- Distribute keywords across introduction, body, and conclusion"
            "\n- Integrate keywords naturally into sentences"
            "\n- Use keywords in varied contexts"
            "\n- Ensure keywords appear in meaningful, informative sentences"
        )
    
    # Quality requirements
    instruction_parts.append(
        "\n\nQUALITY REQUIREMENTS:"
        "\n- Write in a professional, engaging tone"
        "\n- Include proper introduction, body sections, and conclusion"
        "\n- Complete all sentences and paragraphs (no abrupt endings)"
        "\n- Provide detailed explanations and examples"
        "\n- Maintain logical flow and coherence"
        "\n- Ensure the article is informative and comprehensive"
    )
    
    enhanced_prompt = ''.join(instruction_parts)
    return enhanced_prompt
```

**Algorithm Pseudocode**:
```
DMK(prompt, keywords, generated_text):
    IF generated_text is None:
        // Pre-generation: Enhance prompt
        1. Categorize keywords into single/phrase
        2. Build instruction template
        3. Add keyword requirements
        4. Add quality guidelines
        5. Return enhanced_prompt
    ELSE:
        // Post-generation: Validate
        1. Initialize metrics structure
        2. Divide text into thirds
        3. For each keyword:
            a. Count occurrences
            b. Check distribution across sections
            c. Validate context quality
            d. Store detailed analysis
        4. Calculate aggregate metrics
        5. Determine success based on criteria
        6. Return (success, missing, metrics)
```

---

### 2.5 Metrics Module: test_results.py

#### 2.5.1 Module Overview
- **File**: `test_results.py`
- **Purpose**: Calculate, log, and aggregate performance metrics
- **Dependencies**: json, re, statistics, collections.Counter, datetime

#### 2.5.2 Core Functions

```python
import json
import re
import statistics
from collections import Counter
from datetime import datetime

def extract_keywords(text: str, top_n: int = 10) -> list:
    """
    Simple keyword extraction for metrics calculation
    
    Args:
        text (str): Input text
        top_n (int): Number of keywords to return
        
    Returns:
        list: Top N keywords by frequency
    """
    stopwords = {
        "the", "is", "in", "and", "to", "of", "a", "for", 
        "on", "with", "as", "by", "an", "are"
    }
    words = re.findall(r'\w+', text.lower())
    freq = Counter(
        w for w in words 
        if w not in stopwords and len(w) > 3
    )
    return [w for w, _ in freq.most_common(top_n)]


def keyword_accuracy(predicted: list, reference: list) -> float:
    """
    Calculate keyword overlap percentage
    
    Args:
        predicted (list): Predicted keywords
        reference (list): Reference keywords
        
    Returns:
        float: Percentage overlap
        
    Formula:
        accuracy = (|predicted ∩ reference| / |predicted|) × 100
    """
    pred_set = set(map(str.lower, predicted))
    ref_set = set(map(str.lower, reference))
    
    if not pred_set:
        return 0.0
    
    overlap = len(pred_set & ref_set)
    accuracy = (overlap / len(pred_set)) * 100
    
    return round(accuracy, 2)


def keyword_enforcement(text: str, required: list) -> float:
    """
    Calculate percentage of required keywords present
    
    Args:
        text (str): Generated text
        required (list): Required keywords
        
    Returns:
        float: Percentage of keywords present
        
    Formula:
        enforcement = ((total - missing) / total) × 100
    """
    missing = [
        kw for kw in required 
        if kw.lower() not in text.lower()
    ]
    
    enforcement = (
        (len(required) - len(missing)) / len(required)
    ) * 100
    
    return round(enforcement, 2)


def length_metrics(requested: int, text: str) -> dict:
    """
    Calculate word count and vocabulary metrics
    
    Args:
        requested (int): Requested word count
        text (str): Generated text
        
    Returns:
        dict: Length and vocabulary metrics
    """
    words = text.split()
    actual = len(words)
    unique = len(set(w.lower() for w in words))
    
    accuracy = (actual / requested) * 100 if requested > 0 else 0
    unique_ratio = (unique / actual) * 100 if actual > 0 else 0
    
    return {
        "requested": requested,
        "actual": actual,
        "accuracy%": round(accuracy, 2),
        "unique%": round(unique_ratio, 2),
        "target_met": 90 <= accuracy <= 110
    }


def analyze_generation(prompt: str, 
                       generated_text: str,
                       response_time_s: float,
                       requested_words: int) -> dict:
    """
    Complete analysis of a single generation
    
    Args:
        prompt (str): User prompt
        generated_text (str): Generated content
        response_time_s (float): Response time in seconds
        requested_words (int): Requested word count
        
    Returns:
        dict: Comprehensive metrics
    """
    # Extract keywords
    p_kw = extract_keywords(prompt)
    g_kw = extract_keywords(generated_text)
    
    # Build metrics dictionary
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "prompt_keywords": p_kw,
        "generated_keywords": g_kw,
        "keyword_accuracy%": keyword_accuracy(p_kw, g_kw),
        "keyword_enforcement%": keyword_enforcement(generated_text, p_kw),
        "response_time_s": round(response_time_s, 2),
        "length_metrics": length_metrics(requested_words, generated_text)
    }
    
    return metrics


def log_generation(data: dict, path: str = "generation_logs.json") -> None:
    """
    Append generation metrics to JSON log file
    
    Args:
        data (dict): Metrics to log
        path (str): Log file path
    """
    try:
        with open(path, 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    
    logs.append(data)
    
    with open(path, 'w') as f:
        json.dump(logs, f, indent=2)
    
    print(f"✓ Logged generation ({len(logs)} total)")


def aggregate_metrics(path: str = "generation_logs.json") -> dict:
    """
    Calculate aggregate metrics across all generations
    
    Args:
        path (str): Log file path
        
    Returns:
        dict: Aggregate metrics
    """
    try:
        with open(path, 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"error": "No logs found"}
    
    if not logs:
        return {"error": "Empty log file"}
    
    # Helper function
    avg = lambda vals: round(statistics.mean(vals), 2)
    
    # Extract values
    rt = [log["response_time_s"] for log in logs]
    acc = [log["keyword_accuracy%"] for log in logs]
    enf = [log["keyword_enforcement%"] for log in logs]
    wc = [log["length_metrics"]["accuracy%"] for log in logs]
    uniq = [log["length_metrics"]["unique%"] for log in logs]
    
    # Calculate aggregates
    return {
        "total_generations": len(logs),
        "avg_response_time": avg(rt),
        "avg_keyword_accuracy": avg(acc),
        "avg_keyword_enforcement": avg(enf),
        "avg_word_count_accuracy": avg(wc),
        "avg_unique_word_ratio": avg(uniq),
        "targets_met": {
            "response_time": avg(rt) < 10,
            "keyword_accuracy": avg(acc) >= 85,
            "keyword_enforcement": avg(enf) >= 85
        }
    }


def final_report(path: str = "generation_logs.json") -> None:
    """
    Generate and display final metrics report
    
    Args:
        path (str): Log file path
    """
    try:
        with open(path, 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ No generation logs found")
        return
    
    if not logs:
        print("⚠️  No generations found in logs")
        return
    
    num_gen = len(logs)
    
    # Helper
    avg = lambda vals: round(statistics.mean(vals), 2)
    
    # Extract values (backward compatible)
    rt = [
        log.get("response_time_s", log.get("response_time_seconds", 0))
        for log in logs
    ]
    acc = [
        log.get("keyword_accuracy%", log.get("keyword_accuracy_percent", 0))
        for log in logs
    ]
    enf = [
        log.get("keyword_enforcement%", log.get("keyword_enforcement_percent", 0))
        for log in logs
    ]
    
    wc = []
    uniq = []
    for log in logs:
        lm = log.get("length_metrics", {})
        wc.append(lm.get("accuracy%", lm.get("accuracy_percentage", 0)))
        uniq.append(lm.get("unique%", lm.get("unique_word_ratio", 0)))
    
    # Print report
    print("=" * 80)
    print(f"FINAL METRICS REPORT")
    print("=" * 80)
    print(f"\nTotal Generations Analyzed: {num_gen}")
    print("\n" + "-" * 80)
    print(f"{'Metric':<45} {'Result':<20}")
    print("-" * 80)
    print(f"{'Response Time (Average)':<45} {avg(rt)}s")
    print(f"{'Keyword Accuracy (DCKG)':<45} {avg(acc)}%")
    print(f"{'Keyword Enforcement (DMK)':<45} {avg(enf)}%")
    print(f"{'Word Count Accuracy':<45} {avg(wc)}%")
    print(f"{'Unique Word Ratio (Average)':<45} {avg(uniq)}%")
    print("-" * 80)
    
    # Save report
    report = {
        "total_generations": num_gen,
        "avg_response_time": avg(rt),
        "avg_keyword_accuracy": avg(acc),
        "avg_keyword_enforcement": avg(enf),
        "avg_word_count_accuracy": avg(wc),
        "avg_unique_word_ratio": avg(uniq),
        "all_values": {
            "response_times": rt,
            "keyword_accuracy": acc,
            "keyword_enforcement": enf,
            "word_count_accuracy": wc,
            "unique_word_ratio": uniq
        }
    }
    
    with open("final_metrics_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\nFull report saved to: final_metrics_report.json")
    print("=" * 80)
```

---

## 3. DATA MODELS

### 3.1 Request Model

```python
{
    "prompt": str,        # User's content prompt (required)
    "max_words": int,     # Desired word count 100-2000 (required)
    "domain": str         # Content domain (required)
}
```

### 3.2 Response Model

```python
{
    "text": str,                  # Generated article
    "keywords": List[str],        # Extracted keywords
    "dmk_ok": bool,              # Validation status
    "quality_metrics": {
        "total_keywords": int,
        "present_keywords": int,
        "keyword_density": float,
        "well_distributed": int,
        "context_quality": int,
        "detailed_analysis": Dict[str, Dict]
    }
}
```

### 3.3 Generation Log Model

```python
{
    "timestamp": str,             # ISO-8601 datetime
    "prompt_keywords": List[str],
    "generated_keywords": List[str],
    "keyword_accuracy%": float,
    "keyword_enforcement%": float,
    "response_time_s": float,
    "length_metrics": {
        "requested": int,
        "actual": int,
        "accuracy%": float,
        "unique%": float,
        "target_met": bool
    }
}
```

### 3.4 Final Report Model

```python
{
    "total_generations": int,
    "avg_response_time": float,
    "avg_keyword_accuracy": float,
    "avg_keyword_enforcement": float,
    "avg_word_count_accuracy": float,
    "avg_unique_word_ratio": float,
    "all_values": {
        "response_times": List[float],
        "keyword_accuracy": List[float],
        "keyword_enforcement": List[float],
        "word_count_accuracy": List[float],
        "unique_word_ratio": List[float]
    }
}
```

---

## 4. ERROR HANDLING

### 4.1 Frontend Error Handling

```python
try:
    response = make_api_request(prompt, domain, word_count)
except requests.exceptions.Timeout:
    st.error("❌ Request timed out. Please try again.")
except requests.exceptions.ConnectionError:
    st.error("❌ Cannot connect to backend. Ensure API is running.")
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
```

### 4.2 Backend Error Handling

```python
try:
    response = requests.post(groq_url, headers=headers, json=payload)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    logger.error(f"Groq API HTTP error: {e.response.status_code}")
    return JSONResponse(
        status_code=500,
        content={"error": f"API error: {e.response.text}"}
    )
except requests.exceptions.Timeout:
    logger.error("Groq API timeout")
    return JSONResponse(
        status_code=504,
        content={"error": "Request timeout"}
    )
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

---

## 5. PERFORMANCE OPTIMIZATIONS

### 5.1 Token Calculation

```python
# Optimized token calculation to prevent cut-offs
target_tokens = int((max_words / 0.75) * 1.3)

# Breakdown:
# - Division by 0.75: Convert words to tokens (avg 0.75 words/token)
# - Multiplication by 1.3: Add 30% buffer
# - Result: Ensures complete content without excessive length
```

### 5.2 Keyword Extraction Optimization

```python
# Use Counter for O(n) frequency counting
word_freq = Counter(filtered_words)

# Sort once at the end instead of multiple times
sorted_keywords = sorted(scored_keywords.items(), 
                        key=lambda x: x[1], 
                        reverse=True)
```

### 5.3 Regex Compilation

```python
# For repeated pattern matching, compile regex
pattern = re.compile(r'\b' + re.escape(kw_lower) + r'\b')
occurrences = len(pattern.findall(text_lower))
```

---

## 6. TESTING SPECIFICATIONS

### 6.1 Unit Tests

```python
# test_dckg.py
def test_keyword_extraction():
    prompt = "Artificial intelligence is transforming healthcare"
    keywords = generate_keywords(prompt, "technology", top_n=5)
    assert len(keywords) == 5
    assert "artificial" in keywords or "intelligence" in keywords

# test_dmk.py
def test_prompt_enhancement():
    prompt = "Test prompt"
    keywords = ["keyword1", "keyword2"]
    enhanced = apply_dmk_loss(prompt, keywords)
    assert "keyword1" in enhanced
    assert "keyword2" in enhanced

# test_metrics.py
def test_keyword_accuracy():
    predicted = ["word1", "word2", "word3"]
    reference = ["word1", "word2", "word4"]
    accuracy = keyword_accuracy(predicted, reference)
    assert accuracy == 66.67
```

### 6.2 Integration Tests

```python
# test_api.py
def test_generate_endpoint():
    payload = {
        "prompt": "Test prompt",
        "max_words": 750,
        "domain": "test"
    }
    response = requests.post("http://localhost:8000/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "keywords" in data
```

---

## 7. DEPLOYMENT PROCEDURES

### 7.1 Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
echo GROQ_API_KEY="your-key-here" > .env
```

### 7.2 Starting Services

```bash
# Terminal 1: Start backend
uvicorn llama_api:app --reload --port 8000

# Terminal 2: Start frontend
streamlit run longform_streamlit.py
```

### 7.3 Health Checks

```python
# Backend health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}
```

---

## 8. GLOSSARY OF FUNCTIONS

| Function | Module | Purpose |
|----------|--------|---------|
| `generate_keywords()` | dckg.py | Extract keywords from prompt |
| `apply_dmk_loss()` | dmk.py | Enhance prompt / validate keywords |
| `analyze_generation()` | test_results.py | Calculate metrics for generation |
| `log_generation()` | test_results.py | Save metrics to JSON |
| `aggregate_metrics()` | test_results.py | Calculate average metrics |
| `final_report()` | test_results.py | Generate comprehensive report |
| `make_api_request()` | longform_streamlit.py | Send request to backend |
| `generate()` | llama_api.py | Main API endpoint handler |

---

## 9. REVISION HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Aug 30, 2025 | Initial Team | Initial LLD creation |
| 2.0 | Nov 6, 2025 | Sanskriti Rai | Complete rewrite with current implementation details |

---

**END OF LOW-LEVEL DESIGN DOCUMENT**
