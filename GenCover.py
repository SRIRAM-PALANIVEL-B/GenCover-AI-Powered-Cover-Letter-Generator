import streamlit as st
import os
import requests
import docx
import random
import time
import logging
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_community.document_loaders import PyPDFLoader
import tiktoken
from fake_useragent import UserAgent
import psycopg2  # Use for PostgreSQL or switch to MySQL
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key not found. Please set it before proceeding.")
    st.stop()

# Initialize LLM Model
llm_model = "gpt-4o"
llm = ChatOpenAI(temperature=0.0, model=llm_model, openai_api_key=openai_api_key)

def count_tokens(text, model=llm_model):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text)) if isinstance(text, str) else 0

# Define prompts
prompt_job_description = ChatPromptTemplate.from_template("""
    Your role is a tech job researcher. Extract key insights from {job_description}.
""")

prompt_profiler = ChatPromptTemplate.from_template("""
    Your role is a Personal Profiler. Analyze the resume and LinkedIn profile.
    Resume: {resume}
    LinkedIn Profile: {linkedin} (if available)
""")

prompt_cover_letter_composer = ChatPromptTemplate.from_template("""
    Your role is a Cover Letter Writer. Generate a professional cover letter.
    Personal Profile: {personal_profile}
    Job Description: {job_summary}
    Cover Letter Template: {cover_letter_format} (if available)
""")

prompt_proof_reader = ChatPromptTemplate.from_template("""
    Your role is a proofreader. Ensure grammatical correctness and clarity.
    Cover Letter Draft: {cover_letter_draft}
    Cover Letter Template: {cover_letter_format} (if available)
""")

# Define LLM Chains
chain_one = LLMChain(llm=llm, prompt=prompt_job_description, output_key="job_summary")
chain_two = LLMChain(llm=llm, prompt=prompt_profiler, output_key="personal_profile")
chain_three = LLMChain(llm=llm, prompt=prompt_cover_letter_composer, output_key="cover_letter_draft")
chain_four = LLMChain(llm=llm, prompt=prompt_proof_reader, output_key="cover_letter_final")

sequential_chain = SequentialChain(
    chains=[chain_one, chain_two, chain_three, chain_four],
    input_variables=["resume", "linkedin", "job_description", "cover_letter_format"],
    output_variables=["job_summary", "personal_profile", "cover_letter_draft", "cover_letter_final"],
    verbose=True
)

def extract_text_from_pdf(file):
    try:
        temp_path = f"./temp_{file.name}"
        with open(temp_path, "wb") as f:
            f.write(file.getvalue())
        loader = PyPDFLoader(temp_path)
        text = "\n".join([page.page_content for page in loader.load()])
        os.remove(temp_path)
        return text
    except Exception:
        logging.error("Error extracting text from PDF", exc_info=True)
        return ""

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def fetch_job_description(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text(strip=True)
    except requests.exceptions.RequestException:
        return None

def fetch_linkedin_profile(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    try:
        time.sleep(random.uniform(2, 5))
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.exceptions.RequestException:
        return None

def cover_letter_gen(resume_file, linkedin_url, job_description_url, manual_job_description, cover_letter_file):
    resume_content = extract_text_from_pdf(resume_file) if resume_file else ""
    job_description = fetch_job_description(job_description_url) or manual_job_description.strip()
    linkedin_profile = fetch_linkedin_profile(linkedin_url) or ""
    cover_letter_format = extract_text_from_docx(cover_letter_file) if cover_letter_file else ""

    inputs = {"resume": resume_content, "linkedin": linkedin_profile, "job_description": job_description, "cover_letter_format": cover_letter_format}
    try:
        outputs = sequential_chain(inputs)
        return outputs["cover_letter_final"]
    except Exception as e:
        return f"Error: {str(e)}"

def save_to_db(name, email, cover_letter):
    try:
        conn = psycopg2.connect(dbname='your_db', user='your_user', password='your_password', host='your_host', port='your_port')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cover_letters (name, email, content) VALUES (%s, %s, %s)", (name, email, cover_letter))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Database Error: {str(e)}")

# Streamlit UI with Vibrant Colors
st.set_page_config(page_title="GenCover", layout="wide")
st.markdown("""
    <style>
        .main { background-color: #1e1e2e; color: #ffffff; }
        .stTextInput, .stTextArea { border-radius: 10px; background-color: #2a2a3b; color: white; }
        .stButton > button { background-color: #ff6b6b; color: white; font-size: 16px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 GenCover: AI-Powered Cover Letter Generator")
st.sidebar.header("Upload Your Documents")
resume_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])
cover_letter_file = st.sidebar.file_uploader("Upload Cover Letter Template (DOCX)", type=["docx"])
st.sidebar.header("Job Details")
linkedin_url = st.sidebar.text_input("LinkedIn Profile URL (Optional)")
job_description_url = st.sidebar.text_input("Job Description URL")
man_job_desc = st.sidebar.text_area("Or Enter Job Description Manually")
st.sidebar.header("Personal Information")
name = st.sidebar.text_input("Your Name")
email = st.sidebar.text_input("Your Email")
if st.sidebar.button("Generate Cover Letter"):
    if resume_file and (job_description_url or man_job_desc):
        cover_letter = cover_letter_gen(resume_file, linkedin_url, job_description_url, man_job_desc, cover_letter_file)
        save_to_db(name, email, cover_letter)
        st.text_area("Generated Cover Letter", cover_letter, height=300)
    else:
        st.sidebar.error("Please upload a resume and provide job details.")
