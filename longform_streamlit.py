import streamlit as st
import time
import requests
import json
import os
from test_results import analyze_generation, log_generation

st.set_page_config(
    page_title="Freeform Text Generation for Content Creators",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown(
    """
    <style>
    body, .stApp {
        background: radial-gradient(ellipse at top left, #0f2027 0%, #2c5364 60%, #181818 100%);
        color: #e0e0e0;
        font-family: 'Orbitron', 'Share Tech Mono', 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        letter-spacing: 1.2px;
    }
    .stTextInput>div>div>input, .stTextArea textarea {
        font-size: 1.22rem;
        background: linear-gradient(90deg, #23272f 0%, #0f2027 100%);
        color: #39ff14;
        border-radius: 12px;
        border: 1.5px solid #39ff14;
        padding: 1em 1.2em;
        min-height: 48px;
        box-shadow: 0 0 12px #39ff1444, 0 0 2px #ff00cc44;
        text-shadow: 0 0 2px #39ff14, 0 0 8px #ff00cc;
    }
    .stTextArea textarea {
        min-height: 120px !important;
    }
    .stTextInput label, .stTextArea label {
        color: #ff00cc !important;
        font-size: 1.18rem !important;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 0.3em;
        text-shadow: 0 0 4px #ff00cc88;
    }
    .stSlider .rc-slider-track {
        background: linear-gradient(90deg, #39ff14 0%, #ff00cc 100%);
        box-shadow: 0 0 8px #39ff1444;
    }
    .stSlider .rc-slider-handle {
        border-color: #ff00cc;
        background: linear-gradient(135deg, #39ff14 0%, #ff00cc 100%);
        box-shadow: 0 0 12px #ff00cc88, 0 0 8px #39ff1444;
    }
    /* Force Generate button to match Download button exactly */
    .stButton > button, 
    div[data-testid="stButton"] > button,
    .stButton button {
        background: linear-gradient(90deg, #0f2027 0%, #ff00cc 100%) !important;
        color: #39ff14 !important;
        font-size: 1.18rem !important;
        font-family: 'Orbitron', 'Share Tech Mono', 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 0.9em 2.5em !important;
        margin-top: 1em !important;
        border: 2px solid #39ff14 !important;
        box-shadow: 0 0 16px #ff00cc88, 0 0 8px #39ff1444 !important;
        transition: background 0.2s, color 0.2s, box-shadow 0.2s !important;
        letter-spacing: 1px !important;
        text-shadow: 0 0 2px #39ff14, 0 0 8px #ff00cc !important;
        width: auto !important;
        height: auto !important;
    }
    .stButton > button:hover,
    div[data-testid="stButton"] > button:hover,
    .stButton button:hover {
        background: linear-gradient(90deg, #ff00cc 0%, #39ff14 100%) !important;
        color: #0f2027 !important;
        box-shadow: 0 0 32px #ff00cc, 0 0 16px #39ff14 !important;
    }
    .stButton > button:active,
    div[data-testid="stButton"] > button:active,
    .stButton button:active {
        background: linear-gradient(90deg, #39ff14 0%, #ff00cc 100%) !important;
        color: #ff00cc !important;
        box-shadow: 0 0 24px #39ff14, 0 0 12px #ff00cc !important;
    }
    .stDownloadButton>button {
        background: linear-gradient(90deg, #0f2027 0%, #ff00cc 100%) !important;
        color: #39ff14 !important;
        font-size: 1.18rem !important;
        font-family: 'Orbitron', 'Share Tech Mono', 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 0.9em 2.5em !important;
        margin-top: 1em !important;
        border: 2px solid #39ff14 !important;
        box-shadow: 0 0 16px #ff00cc88, 0 0 8px #39ff1444 !important;
        transition: background 0.2s, color 0.2s, box-shadow 0.2s !important;
        letter-spacing: 1px !important;
        text-shadow: 0 0 2px #39ff14, 0 0 8px #ff00cc !important;
    }
    .stDownloadButton>button:hover {
        background: linear-gradient(90deg, #ff00cc 0%, #39ff14 100%) !important;
        color: #0f2027 !important;
        box-shadow: 0 0 32px #ff00cc, 0 0 16px #39ff14 !important;
    }
    .stDownloadButton>button:active {
        background: linear-gradient(90deg, #39ff14 0%, #ff00cc 100%) !important;
        color: #ff00cc !important;
        box-shadow: 0 0 24px #39ff14, 0 0 12px #ff00cc !important;
    }
    .stMarkdown, .stSuccess, .stWarning, .stError {
        font-size: 1.18rem;
        color: #39ff14;
        text-shadow: 0 0 2px #39ff14, 0 0 8px #ff00cc;
    }
    /* Override Streamlit's default success styling */
    .stSuccess,
    .stSuccess > div,
    .stSuccess > div > div,
    .stSuccess .element-container,
    div[data-testid="alert"] {
        background: linear-gradient(90deg, #0f2027 0%, #23272f 100%) !important;
        border: 1px solid #39ff14 !important;
        color: #39ff14 !important;
        border-radius: 12px !important;
        box-shadow: 0 0 16px #39ff1444, 0 0 8px #ff00cc44 !important;
        text-shadow: 0 0 2px #39ff14 !important;
        font-family: 'Orbitron', 'Share Tech Mono', 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        letter-spacing: 0.5px !important;
        padding: 0.75rem 1rem !important;
    }
    .stSuccess p,
    .stSuccess div p,
    .stSuccess .element-container p,
    div[data-testid="alert"] p {
        color: #39ff14 !important;
        text-shadow: 0 0 2px #39ff14 !important;
        font-family: 'Orbitron', 'Share Tech Mono', 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        margin: 0 !important;
    }
    .stWarning,
    .stWarning > div,
    .stWarning > div > div {
        background: linear-gradient(90deg, #0f2027 0%, #2d1b00 100%) !important;
        border: 1px solid #ff9500 !important;
        color: #ff9500 !important;
        border-radius: 12px !important;
        box-shadow: 0 0 16px #ff950044, 0 0 8px #ff00cc44 !important;
        text-shadow: 0 0 2px #ff9500 !important;
        font-family: 'Orbitron', 'Share Tech Mono', 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .stError,
    .stError > div,
    .stError > div > div {
        background: linear-gradient(90deg, #0f2027 0%, #2d0000 100%) !important;
        border: 1px solid #ff0040 !important;
        color: #ff0040 !important;
        border-radius: 12px !important;
        box-shadow: 0 0 16px #ff004044, 0 0 8px #ff00cc44 !important;
        text-shadow: 0 0 2px #ff0040 !important;
    }
    h1 {
        font-size: 2.8rem;
        font-family: 'Orbitron', 'Share Tech Mono', 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        font-weight: 900;
        color: #ff00cc;
        margin-bottom: 0.7em;
        letter-spacing: 2px;
        text-shadow: 0 0 12px #ff00cc, 0 0 8px #39ff14;
        border-bottom: 2px solid #39ff14;
        padding-bottom: 0.3em;
    }
    label, .stSlider label {
        color: #39ff14 !important;
        font-size: 1.18rem;
        text-shadow: 0 0 4px #39ff1488;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>Freeform Text Generation for Content Creators</h1>", unsafe_allow_html=True)

# quick count of existing generations
try:
    if os.path.exists("generation_logs.json"):
        with open("generation_logs.json", 'r', encoding='utf-8') as f:
            logs = json.load(f)
            num_generations = len(logs)
    else:
        num_generations = 0
except Exception:
    num_generations = 0

prompt = st.text_area("Enter your prompt for longform text:", height=180)
domain = st.text_input("Enter domain (e.g. education, marketing, technology, etc.):")
word_count = st.slider("Desired word count:", min_value=750, max_value=2000, value=750, step=50)

API_URL = "http://localhost:8000/generate"

if st.button("Generate", help="Generate longform text using your context and domain"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating text..."):
            try:
                start_time = time.time()
                
                response = requests.post(
                    API_URL,
                    json={
                        "prompt": prompt,
                        "max_words": word_count,
                        "domain": domain
                    }
                )
                
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    long_text = response.json().get("text", "")
                    
                    analysis = analyze_generation(
                        prompt=prompt,
                        generated_text=long_text,
                        response_time_s=response_time,
                        requested_words=word_count
                    )

                    log_generation(analysis)

                    actual_words = len(long_text.split())
                    st.markdown(f"""
                    <div style='
                        background: linear-gradient(90deg, #0f2027 0%, #23272f 100%);
                        border: 1px solid #39ff14;
                        color: #39ff14;
                        border-radius: 12px;
                        padding: 0.75rem 1rem;
                        margin: 1rem 0;
                        box-shadow: 0 0 16px #39ff1444, 0 0 8px #ff00cc44;
                        text-shadow: 0 0 2px #39ff14;
                        font-family: "Orbitron", "Share Tech Mono", "Inter", sans-serif;
                        letter-spacing: 0.5px;
                        font-size: 1.18rem;
                    '>
                        ✅ Generated {actual_words} words in {response_time:.2f}s 
                        | Keyword Match: {analysis['keyword_enforcement%']:.1f}% 
                        | Unique Words: {analysis['length_metrics']['unique%']:.1f}%
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display generated text
                    st.markdown(f"<div style='font-size:1.25rem;line-height:1.8;background:linear-gradient(90deg, #0f2027 0%, #23272f 100%);padding:1.5em 1.2em;border-radius:14px;border:1px solid #39ff14;color:#39ff14;margin-top:1em;box-shadow:0 0 16px #39ff1444, 0 0 8px #ff00cc44;text-shadow:0 0 2px #39ff14'>{long_text}</div>", unsafe_allow_html=True)
                    
                    with st.expander("📊 View Detailed Metrics"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Response Time", f"{response_time:.2f}s", 
                                     delta="Target: <10s", delta_color="normal")
                            st.metric("Requested Words", word_count)
                            st.metric("Actual Words", actual_words)
                        
                        with col2:
                            st.metric("Keyword Accuracy", f"{analysis['keyword_accuracy%']:.1f}%",
                                     delta="Target: >85%", delta_color="normal")
                            st.metric("Keyword Enforcement", f"{analysis['keyword_enforcement%']:.1f}%",
                                     delta="Target: >85%", delta_color="normal")
                            st.metric("Word Count Accuracy", f"{analysis['length_metrics']['accuracy%']:.1f}%")
                        
                        with col3:
                            st.metric("Total Words", analysis['length_metrics']['actual'])
                            st.metric("Unique Words", int(analysis['length_metrics']['actual'] * analysis['length_metrics']['unique%'] / 100))
                            st.metric("Unique Word Ratio", f"{analysis['length_metrics']['unique%']:.1f}%")
                        
                        st.write("**Extracted Keywords from Prompt:**")
                        st.write(", ".join(analysis['prompt_keywords'][:10]))
                        
                        st.write("**Keywords Found in Generated Text:**")
                        st.write(", ".join(analysis['generated_keywords'][:10]))

                    st.download_button("Download text", long_text, file_name="longform.txt")
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error connecting to Llama API: {e}")