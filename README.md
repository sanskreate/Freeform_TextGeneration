# 🌐 FreeForm Long Text Generation

A cyberpunk-themed AI-powered text generation platform for content creators, featuring intelligent keyword extraction and enforcement for high-quality, domain-specific content generation.

## 🚀 Demo

[![Watch Demo Video](https://img.shields.io/badge/📺_Watch_Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/5kXg4Cr8-oE)

**Live Demo:** [Watch on YouTube](https://youtu.be/5kXg4Cr8-oE)

## ✨ Features

### 🎯 Core Functionality
- **AI-Powered Text Generation**: Leveraging Groq's Llama 3 model for high-quality content creation
- **Domain-Specific Generation**: Specialized content for Technology, Health, Finance, and Education sectors
- **Intelligent Keyword Extraction**: DCKG (Domain-Centric Keyword Generation) algorithm
- **Keyword Enforcement**: DMK (Domain-aware Model for Keyword enforcement) validation
- **Customizable Word Count**: Flexible text length from 100 to 2000 words

### 🎨 Cyberpunk UI Experience
- **Futuristic Design**: Neon green (#39ff14) and pink (#ff00cc) color scheme
- **Orbitron Typography**: Professional sci-fi font styling
- **Glowing Effects**: Animated borders and interactive elements
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Accessibility Compliant**: WCAG 2.1 AA standards

### 🔧 Technical Features
- **Fast API Backend**: High-performance asynchronous API
- **Streamlit Frontend**: Interactive and user-friendly interface
- **Real-time Processing**: Live status updates and progress indicators
- **Download Functionality**: Export generated content as .txt files
- **Error Handling**: Comprehensive validation and user feedback

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External AI   │
│  (Streamlit)    │◄──►│   (FastAPI)     │◄──►│   (Groq API)    │
│                 │    │                 │    │                 │
│ • User Interface│    │ • DCKG Module   │    │ • Llama 3 Model │
│ • Cyberpunk UI  │    │ • DMK Module    │    │ • Text Gen      │
│ • File Download │    │ • API Routes    │    │ • Chat Completion│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Interactive web interface |
| **Backend** | FastAPI | REST API and business logic |
| **AI Model** | Groq Llama 3 | Text generation engine |
| **Styling** | Custom CSS | Cyberpunk theme implementation |
| **Language** | Python 3.8+ | Core development language |

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key (sign up at [Groq](https://groq.com/))

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Freeform_TextGeneration.git
   cd Freeform_TextGeneration
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

5. **Start the backend**
   ```bash
   uvicorn llama_api:app --reload --port 8000
   ```

6. **Launch the frontend** (in a new terminal)
   ```bash
   streamlit run longform_streamlit.py
   ```

7. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
API_BASE_URL=http://localhost:8000
MODEL_NAME=llama3-8b-8192
MAX_TOKENS=2000
TEMPERATURE=0.7
```

## 📝 Usage

### Basic Text Generation

1. **Enter your prompt**: Describe the content you want to generate
2. **Select domain**: Choose from Technology, Health, Finance, or Education
3. **Set word count**: Use the slider to specify desired length (100-2000 words)
4. **Generate**: Click the "🚀 GENERATE TEXT" button
5. **Download**: Save the generated content as a .txt file

### API Usage

The backend provides RESTful APIs for integration:

```python
import requests

# Generate text via API
response = requests.post("http://localhost:8000/generate", json={
    "prompt": "Explain quantum computing",
    "domain": "Technology",
    "max_words": 500
})

result = response.json()
print(result["generated_text"])
```

## 🏃‍♂️ Development

### Project Structure

```
neural-text-synthesizer/
├── 📁 docs/                    # Documentation
│   ├── HLD_Document.md         # High-Level Design
│   ├── LLD_Document.md         # Low-Level Design
│   ├── Architecture_Document.md # System Architecture
│   └── Wireframe_Document.md   # UI/UX Specifications
├── 📄 longform_streamlit.py    # Frontend application
├── 📄 llama_api.py            # Backend API server
├── 📄 dckg.py                 # Keyword extraction module
├── 📄 dmk.py                  # Keyword enforcement module
├── 📄 requirements.txt        # Python dependencies
├── 📄 .env                    # Environment variables
└── 📄 README.md              # This file
```

### Key Modules

#### DCKG (Domain-Centric Keyword Generation)
- Extracts relevant keywords from user prompts
- Filters and ranks keywords by importance
- Provides domain-specific keyword suggestions

#### DMK (Domain-aware Model for Keyword enforcement)
- Validates generated content for keyword presence
- Ensures content meets domain requirements
- Provides feedback on missing keywords

### Development Server

```bash
# Backend with hot reload
uvicorn llama_api:app --reload --port 8000

# Frontend with auto-refresh
streamlit run longform_streamlit.py --server.runOnSave true
```

## 🔍 API Documentation

### Endpoints

#### POST `/generate`

Generate text based on user input.

**Request Body:**
```json
{
  "prompt": "Your content description",
  "domain": "Technology",
  "max_words": 500
}
```

**Response:**
```json
{
  "generated_text": "Generated content...",
  "word_count": 487,
  "keywords_found": ["AI", "machine learning", "algorithms"],
  "status": "success"
}
```

## 🎨 UI Components

### Cyberpunk Theme

The application features a distinctive cyberpunk aesthetic:

- **Neon Colors**: Electric green (#39ff14) and hot pink (#ff00cc)
- **Glowing Effects**: Animated borders and hover states
- **Typography**: Orbitron font family for futuristic appeal
- **Dark Theme**: High contrast for visual impact
- **Smooth Animations**: 60fps interactions and transitions

### Responsive Design

- **Desktop**: Side-by-side input/output layout
- **Tablet**: Stacked layout with optimized spacing
- **Mobile**: Single-column design with touch-friendly controls

## 🚀 Deployment

### Production Considerations

- Use environment-specific configuration
- Implement proper logging and monitoring
- Set up load balancing for high traffic
- Configure HTTPS with SSL certificates
- Implement rate limiting and API quotas

## 🧪 Testing

### Manual Testing Checklist

- [ ] Text generation with different prompts
- [ ] All domain selections work correctly
- [ ] Word count slider functions properly
- [ ] Download functionality works
- [ ] Error handling for invalid inputs
- [ ] Responsive design on different screen sizes
- [ ] Accessibility features (keyboard navigation, screen readers)

### Development Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 📊 Performance

### Benchmarks

- **Text Generation**: < 10 seconds for 1000 words
- **Frontend Load Time**: < 2 seconds
- **API Response Time**: < 500ms (excluding AI generation)
- **Memory Usage**: < 512MB per instance

### Optimization Features

- Async API operations for better concurrency
- Efficient keyword processing algorithms
- Streamlit caching for improved performance
- Responsive design for all devices

## 🔒 Security

### Data Protection

- No user data stored permanently
- API keys secured via environment variables
- Input validation and sanitization
- HTTPS encryption in production

### Privacy

- No tracking or analytics
- User prompts not logged
- Generated content not retained
- Compliance with data protection regulations

## 🐛 Troubleshooting

### Common Issues

**Q: Text generation fails**
- Check your Groq API key in `.env` file
- Verify internet connection
- Ensure API quota is not exceeded

**Q: Frontend won't start**
- Confirm Streamlit is installed: `pip install streamlit`
- Check if port 8501 is available
- Verify Python version (3.8+ required)

**Q: Backend connection error**
- Ensure FastAPI server is running on port 8000
- Check firewall settings
- Verify backend URL in frontend configuration

### Debug Mode

```bash
# Enable debug logging
export DEBUG=1
streamlit run longform_streamlit.py --logger.level debug
```

### Long-term Vision

- Integration with popular content management systems
- Advanced AI models for specialized domains
- Collaborative content creation features
- Enterprise deployment options

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** for providing the powerful Llama 3 API
- **Streamlit** for the excellent web framework
- **FastAPI** for the high-performance backend framework
- **Open Source Community** for the amazing tools and libraries
