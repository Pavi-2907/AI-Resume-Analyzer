# 🚀 AI Resume Analyzer

An AI-powered Resume Screening and Candidate Evaluation System built using Flask and Large Language Models (LLMs).

This project automates the resume analysis process by extracting candidate information from resumes, matching skills with job descriptions, calculating compatibility scores, generating AI-based insights, creating interview questions, and providing career improvement suggestions.

---

# 📌 Project Overview

Recruiters often spend significant time manually screening resumes and evaluating candidates.

This project simplifies the hiring process by using AI and automation to:

✅ Extract resume data  
✅ Compare resumes with Job Descriptions (JD)  
✅ Identify matched and missing skills  
✅ Calculate candidate-job compatibility scores  
✅ Generate AI-powered recruiter insights  
✅ Generate interview questions automatically  
✅ Provide resume improvement tips  
✅ Suggest career roadmaps for candidates  

---

# ✨ Key Features

## 👨‍💼 Recruiter Module
- Upload candidate resume
- Paste Job Description
- Extract candidate details automatically
- Skill matching and missing skill detection
- AI-generated candidate summary
- Match percentage calculation
- Interview question generation
- Download interview questions as PDF

---

## 👨‍🎓 Candidate Module
- Resume evaluation
- AI-based resume feedback
- Career roadmap generation
- Skill gap analysis
- Overall fit analysis

---

# 🧠 AI Functionalities

This project uses LLM-based prompt engineering to generate:

- Candidate summaries
- Interview questions
- Resume improvement suggestions
- Career roadmap recommendations

The AI model used:
- **Groq API**
- **Llama-3.3-70B-Versatile**

---

# ⚙️ Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend Logic |
| Flask | Web Framework |
| HTML/CSS | Frontend UI |
| Groq API | AI Integration |
| Llama 3.3 70B | Large Language Model |
| pdfplumber | PDF Text Extraction |
| Regex | Information Extraction |
| FPDF | PDF Generation |

---

# 🔄 Complete Project Workflow

## Step 1 — Resume Upload
User uploads a PDF resume and enters a Job Description.

---

## Step 2 — PDF Text Extraction
The uploaded resume is processed using `pdfplumber`.

The system extracts text content from every page of the PDF.

---

## Step 3 — Candidate Information Extraction
Using Regular Expressions (Regex), the system extracts:

- Name
- Email
- Phone Number
- Education
- Experience

---

## Step 4 — Skill Matching
The system compares resume skills with Job Description skills using predefined technical skill lists.

### Output:
- Matched Skills
- Missing Skills
- Match Percentage

---

## Step 5 — Score Calculation

The system calculates:

- Skill Match Score
- Education Score
- Experience Score
- Overall Candidate Fit Score

---

## Step 6 — AI Insights Generation

Using Groq LLM APIs, the system generates:

- Candidate Summary
- Resume Improvement Tips
- Career Roadmap
- Interview Questions

---

## Step 7 — PDF Generation

Interview questions are converted into downloadable PDF format using FPDF.

---

# 📊 Skill Matching Logic

The project uses a keyword-based skill matching algorithm.

### Formula Used

```text
Match Percentage = (Matched Skills / JD Skills) × 100
```

# 🎯 Future Improvements

- OCR support for image resumes
- Database integration
- User authentication
- Resume ranking system
- ATS compatibility analysis
- Cloud deployment
---

# 💡 Why This Project?

This project demonstrates practical implementation of:

- AI Integration
- LLM Prompt Engineering
- NLP Concepts
- Flask Backend Development
- Resume Parsing
- Regex Processing
- PDF Processing
- Real-world Recruitment Automation

---

# 👩‍💻 Author

Pavithra K 


