# Resume Optimizer & ATS Analyzer

An AI-powered tool that analyzes resumes against job descriptions, provides ATS compatibility scores, identifies keyword gaps, and suggests improvements.

## Features

- ATS Score Calculation (0-100 scale)
- Keyword Analysis with visual highlighting
- Matched keywords (green) and missing keywords (red)
- Detailed improvement suggestions
- AI-generated rephrased resume version
- Real-time analysis using Google Gemini AI

## Technology Stack

- Python 3.8+
- Streamlit (Web Interface)
- Google Gemini 2.5 Flash (AI Model)
- PyMuPDF (PDF Processing)

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available)
- pip package manager

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Anu-662/cv-fit-analyzer
cd cv-fit-analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root directory:
```
GEMINI_API_KEY=your_api_key_here
```

**How to get your API key:**

1. Visit https://aistudio.google.com/
2. Sign in with your Google account
3. Click "Get API Key"
4. Create a new API key or use an existing project
5. Copy the key and paste it in your `.env` file

## Usage

### Run the application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the tool

1. Upload your resume in PDF format
2. Paste the complete job description in the text area
3. Click "Analyze Resume"
4. Review results across three tabs:
   - ATS Score & Keywords
   - Suggested Improvements
   - Rephrased Resume

## API Usage Limits

### Free Tier
- 1,500 requests per day
- 15 requests per minute
- 1 million tokens per minute

### Token Usage per Analysis
- ATS Score: ~2,000-5,000 tokens
- Keyword Analysis: ~2,000-4,000 tokens
- Improvement Suggestions: ~3,000-6,000 tokens
- Resume Rephrasing: ~5,000-15,000 tokens

**Total per complete analysis:** ~12,000-30,000 tokens

With the free tier, you can analyze approximately 50-100 resumes per day.

### Paid Tier Pricing
