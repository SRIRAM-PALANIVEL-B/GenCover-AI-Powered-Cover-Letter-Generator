# GenCover-AI-Powered-Cover-Letter-Generator

📌 Project Overview
GenCover is an AI-powered tool that generates personalized, job-specific cover letters by analyzing resumes, LinkedIn profiles, and job descriptions. Using Generative AI (GPT-4o), web scraping, and NLP techniques, it creates high-quality cover letters in minutes, saving time and effort for job seekers.

⚡ Features
✅ Upload resume (PDF)
✅ Fetch job description from a URL or manual input
✅ Extract LinkedIn profile content (optional)
✅ AI-powered cover letter generation using GPT-4o
✅ Proofreading and grammar check
✅ Save cover letters to a database for future use

🛠️ Tech Stack
Programming & Frameworks: Python, Streamlit
AI & NLP: OpenAI GPT-4o, LangChain
Data Processing: BeautifulSoup (Web Scraping), PyPDFLoader (PDF Parsing), python-docx (DOCX Parsing)
Database: PostgreSQL/MySQL
Environment & Deployment: dotenv, GitHub
🔄 Project Workflow
1️⃣ User Input

Upload Resume (PDF)
Enter LinkedIn Profile URL (Optional)
Enter Job Description (URL or manual input)
Upload Cover Letter Template (Optional)
Click Generate Cover Letter
2️⃣ Data Extraction

Extracts resume text
Fetches job description from the URL
Extracts LinkedIn profile data (if provided)
Reads cover letter template (if uploaded)
3️⃣ AI-Powered Cover Letter Generation

Extracts key insights from the job description
Analyzes job responsibilities, required skills, and qualifications
Generates a structured and personalized cover letter
Proofreads and refines the cover letter for clarity and correctness
4️⃣ Save & Display Cover Letter

Displays the generated cover letter
Saves it in a PostgreSQL/MySQL database



🚀 Future Enhancements
✅ Add email integration for sending cover letters
✅ Store and retrieve previous cover letters for users
✅ Implement user authentication for personalized history
✅ Improve LinkedIn profile extraction using API instead of scraping

🏆 Why Use GenCover?
✅ Saves Time – No need to manually write new cover letters for every job
✅ Professional Output – Ensures well-structured, role-specific content
✅ Personalized – AI tailors the cover letter to job descriptions
✅ Fully Automated – Generates cover letters in minutes




# 💻 How to Run Locally

# Clone the repository
      git clone https://github.com/yourusername/GenCover.git
      cd GenCover

# Install dependencies
    pip install streamlit requests python-docx beautifulsoup4 langchain_openai langchain psycopg2-binary tiktoken fake_useragent python-dotenv

# Set up environment variables (.env file)
    OPENAI_API_KEY=your_openai_api_key

# Run the Streamlit app
    streamlit run app.py
