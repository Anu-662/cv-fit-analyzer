import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import fitz
import re

load_dotenv()
genai.configure(api_key="AIzaSyCdJiLcr0B056C-PN1vdoZyLmSNr2dipFI")

st.set_page_config(
    page_title="Resume Optimizer with ATS Score",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Remove top padding and header */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Force light theme */
    .stApp {
        background-color: #ffffff !important;
        color: #262730 !important;
    }
    
    .main .block-container {
        background-color: #ffffff !important;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
        font-size: 1.1rem;
    }
    
    /* Input elements */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #262730 !important;
        border: 1px solid #d0d0d0 !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stFileUploader"] {
        background-color: #f8f9fa !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stFileUploader"] section {
        background-color: #ffffff !important;
        border: 2px dashed #cccccc !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #262730 !important;
    }
    
    /* Button */
    .stButton button {
        background-color: #1f77b4 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 0.75rem 2rem !important;
    }
    
    /* Subheaders */
    .stApp h2, .stApp h3 {
        color: #262730 !important;
        font-weight: 600 !important;
    }
    
    /* Tabs - Clean modern style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: #ffffff;
        border-bottom: 2px solid #e0e0e0;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #666666 !important;
        border-radius: 0;
        padding: 12px 24px;
        font-weight: 500;
        border-bottom: 3px solid transparent;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f5f5f5;
        color: #262730 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #1f77b4 !important;
        border-bottom: 3px solid #1f77b4 !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #ffffff;
        color: #262730;
        padding-top: 2rem;
    }
    
    /* Keyword badges */
    .keyword-matched {
        background-color: #d4edda;
        color: #155724;
        padding: 6px 12px;
        border-radius: 6px;
        margin: 4px;
        display: inline-block;
        font-weight: 500;
        font-size: 0.9rem;
        border: 1px solid #c3e6cb;
    }
    
    .keyword-missing {
        background-color: #f8d7da;
        color: #721c24;
        padding: 6px 12px;
        border-radius: 6px;
        margin: 4px;
        display: inline-block;
        font-weight: 500;
        font-size: 0.9rem;
        border: 1px solid #f5c6cb;
    }
    
    /* Improvement box */
    .improvement-box {
        background-color: #f0f8ff;
        border-left: 4px solid #1f77b4;
        padding: 20px;
        margin: 20px 0;
        border-radius: 8px;
        color: #262730;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        padding-top: 2rem;
    }
    
    section[data-testid="stSidebar"] * {
        color: #262730 !important;
    }
    
    /* Messages */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Markdown */
    .stMarkdown {
        color: #262730 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8f9fa !important;
        color: #262730 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #1f77b4 !important;
    }
    
    /* Column spacing */
    [data-testid="column"] {
        padding: 0 1rem;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border-color: #e0e0e0;
    }
    
    /* All text */
    p, span, div, label {
        color: #262730 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">Resume Optimizer & ATS Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Analyze your resume and get intelligent suggestions for improvement</p>', unsafe_allow_html=True)

def extract_pdf_text(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def analyze_keywords(cv_text, job_text):
    prompt = f"""
    You are an ATS keyword extraction expert.
    
    Analyze the resume and job description to identify important keywords.
    Be consistent and objective. Focus on technical skills, tools, qualifications, and domain-specific terms.
    
    Identify:
    1. Keywords from the job description that ARE present in the resume (MATCHED)
    2. Important keywords from the job description that are MISSING in the resume
    
    Return ONLY a structured list in this exact format:
    
    MATCHED KEYWORDS:
    keyword1, keyword2, keyword3, keyword4, keyword5
    
    MISSING KEYWORDS:
    keyword1, keyword2, keyword3, keyword4, keyword5
    
    Job Description:
    {job_text}
    
    Resume:
    {cv_text}
    """
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    generation_config = {
        "temperature": 0.1,
        "top_p": 0.8,
        "top_k": 40,
    }
    
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )
    return response.text.strip()

def calculate_ats_score(cv_text, job_text):
    prompt = f"""
    You are an ATS (Applicant Tracking System) expert analyzer.
    
    Score this resume using this EXACT rubric for consistency:
    
    KEYWORD MATCHING (40 points):
    - Count important keywords from job description present in resume
    - 35-40 points: 90%+ keywords present
    - 25-34 points: 70-89% keywords present
    - 15-24 points: 50-69% keywords present
    - 0-14 points: Less than 50% keywords present
    
    SKILLS ALIGNMENT (30 points):
    - Evaluate how well candidate's skills match requirements
    - 25-30 points: Skills perfectly match requirements
    - 18-24 points: Most required skills match
    - 10-17 points: Some skills match
    - 0-9 points: Few skills match
    
    EXPERIENCE RELEVANCE (20 points):
    - Assess relevance of work experience
    - 17-20 points: Highly relevant experience
    - 12-16 points: Moderately relevant
    - 6-11 points: Somewhat relevant
    - 0-5 points: Not relevant
    
    FORMAT COMPATIBILITY (10 points):
    - Check ATS-friendly formatting
    - 9-10 points: Perfect ATS format
    - 7-8 points: Good format
    - 4-6 points: Acceptable format
    - 0-3 points: Poor format
    
    Be objective and consistent. Use the same criteria each time.
    
    Job Description:
    {job_text}
    
    Resume Content:
    {cv_text}
    
    Provide your response in this format:
    
    ATS SCORE: [number]/100
    
    ANALYSIS:
    [Detailed explanation of score breakdown by category]
    
    STRENGTHS:
    - Point 1
    - Point 2
    - Point 3
    
    WEAKNESSES:
    - Point 1
    - Point 2
    - Point 3
    """
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    generation_config = {
        "temperature": 0.1,
        "top_p": 0.8,
        "top_k": 40,
    }
    
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )
    return response.text.strip()

def get_improvement_suggestions(cv_text, job_text):
    prompt = f"""
    You are an expert career coach and resume writer.
    
    Provide specific, actionable improvement suggestions for this resume based on the job description.
    
    Format your response with these sections:
    
    SUGGESTED IMPROVEMENTS:
    1. [Specific actionable suggestion with examples]
    2. [Another specific suggestion]
    3. [Continue with 5-8 suggestions total]
    
    RECOMMENDED ADDITIONS:
    - [Specific skills or experiences to add]
    - [Certifications or qualifications to highlight]
    
    RECOMMENDED CHANGES:
    - [What to modify in existing content]
    - [How to restructure sections]
    
    Job Description:
    {job_text}
    
    Resume:
    {cv_text}
    """
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    generation_config = {
        "temperature": 0.3,
        "top_p": 0.9,
        "top_k": 40,
    }
    
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )
    return response.text.strip()

def rephrase_resume(cv_text, job_text):
    prompt = f"""
    You are an expert resume writer.
    
    Rephrase this resume to be optimized for the given job description. Focus on:
    
    1. Incorporate missing keywords naturally
    2. Quantify achievements with metrics
    3. Use strong action verbs
    4. Match the job description's tone and language
    5. Make it ATS-friendly with clear formatting
    6. Highlight relevant experience prominently
    
    Provide the COMPLETE rephrased resume in a professional format.
    Use standard section headers: Professional Summary, Skills, Work Experience, Education
    
    Job Description:
    {job_text}
    
    Original Resume:
    {cv_text}
    
    Return ONLY the rephrased resume content.
    """
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    generation_config = {
        "temperature": 0.4,
        "top_p": 0.9,
        "top_k": 40,
    }
    
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )
    return response.text.strip()

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Upload Resume")
    uploaded_cv = st.file_uploader("Upload your CV (PDF format)", type=["pdf"])

with col2:
    st.subheader("Job Description")
    job_description = st.text_area("Paste the Job Description here", height=200, 
                                    placeholder="Copy and paste the complete job description here...")

st.markdown("---")

if st.button("Analyze Resume", type="primary", use_container_width=True):
    if uploaded_cv and job_description.strip():
        
        with st.spinner("Extracting text from your resume..."):
            cv_text = extract_pdf_text(uploaded_cv)
        
        if not cv_text.strip():
            st.error("Could not extract text from PDF. Please ensure it's a text-based PDF, not a scanned image.")
        else:
            st.success("Resume text extracted successfully")
            st.markdown("")
            
            tab1, tab2, tab3 = st.tabs(["ATS Score & Keywords", "Suggested Improvements", "Rephrased Resume"])
            
            with tab1:
                col_a, col_b = st.columns([1, 1], gap="large")
                
                with col_a:
                    with st.spinner("Calculating ATS score..."):
                        try:
                            ats_result = calculate_ats_score(cv_text, job_description)
                            
                            score_match = re.search(r'ATS SCORE:?\s*(\d+)', ats_result, re.IGNORECASE)
                            
                            if score_match:
                                score = int(score_match.group(1))
                                
                                if score >= 80:
                                    st.success(f"### ATS Score: {score}/100")
                                    st.write("**Excellent** - Your resume is highly ATS-compatible")
                                elif score >= 60:
                                    st.warning(f"### ATS Score: {score}/100")
                                    st.write("**Good** - Some improvements recommended")
                                else:
                                    st.error(f"### ATS Score: {score}/100")
                                    st.write("**Needs Work** - Review suggestions carefully")
                                
                                st.progress(score / 100)
                            
                            st.markdown("")
                            st.markdown(ats_result)
                            
                        except Exception as e:
                            st.error(f"Error analyzing ATS score: {e}")
                
                with col_b:
                    with st.spinner("Analyzing keywords..."):
                        try:
                            keyword_analysis = analyze_keywords(cv_text, job_description)
                            
                            st.subheader("Keyword Analysis")
                            st.markdown("")
                            
                            matched_section = re.search(r'MATCHED KEYWORDS:?\s*\n?(.*?)(?=MISSING KEYWORDS|$)', 
                                                       keyword_analysis, re.IGNORECASE | re.DOTALL)
                            missing_section = re.search(r'MISSING KEYWORDS:?\s*\n?(.*?)$', 
                                                       keyword_analysis, re.IGNORECASE | re.DOTALL)
                            
                            if matched_section:
                                st.markdown("**Matched Keywords**")
                                st.caption("Keywords found in your resume")
                                st.markdown("")
                                matched_keywords = [k.strip() for k in matched_section.group(1).split(',') if k.strip()]
                                
                                keywords_html = ""
                                for keyword in matched_keywords:
                                    keyword = keyword.strip('- •*').strip()
                                    if keyword:
                                        keywords_html += f'<span class="keyword-matched">{keyword}</span> '
                                
                                st.markdown(keywords_html, unsafe_allow_html=True)
                            
                            st.markdown("")
                            st.markdown("")
                            
                            if missing_section:
                                st.markdown("**Missing Keywords**")
                                st.caption("Important keywords to add")
                                st.markdown("")
                                missing_keywords = [k.strip() for k in missing_section.group(1).split(',') if k.strip()]
                                
                                keywords_html = ""
                                for keyword in missing_keywords:
                                    keyword = keyword.strip('- •*').strip()
                                    if keyword:
                                        keywords_html += f'<span class="keyword-missing">{keyword}</span> '
                                
                                st.markdown(keywords_html, unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"Error analyzing keywords: {e}")
            
            with tab2:
                with st.spinner("Generating improvement suggestions..."):
                    try:
                        improvements = get_improvement_suggestions(cv_text, job_description)
                        
                        st.markdown('<div class="improvement-box">', unsafe_allow_html=True)
                        st.markdown("### Suggested Improvements")
                        st.markdown("Review these recommendations to strengthen your resume for this position.")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown(improvements)
                        
                    except Exception as e:
                        st.error(f"Error generating suggestions: {e}")
            
            with tab3:
                with st.spinner("Rephrasing your resume... This may take 20-30 seconds..."):
                    try:
                        rephrased = rephrase_resume(cv_text, job_description)
                        
                        st.info("**Note:** This is an AI-generated rephrased version. Review and customize it before using.")
                        st.markdown("")
                        
                        st.markdown("### Here is the Rephrased Version of Your Resume")
                        st.markdown(rephrased)
                        
                    except Exception as e:
                        st.error(f"Error rephrasing resume: {e}")
    
    else:
        st.warning("Please upload your resume and paste a job description to proceed.")

st.markdown("---")
with st.expander("How it works & Tips"):
    st.markdown("""
    ### How This Tool Works:
    1. Upload Your Resume: PDF format (text-based, not scanned)
    2. Paste Job Description: Complete job posting
    3. Get ATS Score: See how well your resume matches
    4. Review Keywords: See matched (green) and missing (red) keywords
    5. Read Suggestions: Get specific improvement recommendations
    6. View Rephrased Version: See an optimized version of your resume
    
    ### Tips for Best Results:
    - Use a complete, detailed job description
    - Ensure your PDF has selectable text
    - Review all suggestions before making changes
    - The rephrased version is a starting point - customize it
    - Always proofread before submitting
    
    ### ATS Score Breakdown:
    - 80-100: Excellent match
    - 60-79: Good match, minor improvements needed
    - 40-59: Moderate match, significant improvements needed
    - 0-39: Weak match, major revision needed
    
    ### Keyword Colors:
    - Green: Keywords found in your resume
    - Red: Important keywords missing from your resume
    """)

st.sidebar.markdown("### API Usage Limits")
st.sidebar.info("Free tier: 1,500 requests per day")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
This tool uses AI to analyze your resume against job descriptions and provide actionable improvement suggestions.

**Powered by:**
- Google Gemini 2.5 Flash
- Streamlit
""")