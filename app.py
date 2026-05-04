from flask import Flask, render_template, request, send_file
import re
import pdfplumber
from skills import TECHNICAL_SKILLS
from groq import Groq
from fpdf import FPDF

app = Flask(__name__)

# -------- GROQ API -------- #

client = Groq(api_key="GROQ_API_KEY")

# ================= AI CANDIDATE SUMMARY =================

def generate_candidate_summary(details, matched, missing):

    prompt = f"""
You are an AI recruitment assistant.

Analyze the candidate and return ONLY 4-5 short bullet points.

Each point must be ONE LINE only.

Focus on:
• Candidate strengths
• Technical capability
• Job suitability
• Missing skills if any
• One improvement suggestion

Candidate Details:
Name: {details.get("name")}
Education: {details.get("education")}
Experience: {details.get("experience")}

Matched Skills:
{matched}

Missing Skills:
{missing}

Return format example:


• Strong Python and Machine Learning skills
• Good academic background in AI
• Suitable for Junior Data Science roles
• Missing Docker and AWS exposure
• Could improve with more real-world projects
. don't give same this is for example only
. don't give more length , give impotant points only
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message.content

    except:
        summary = "AI summary could not be generated."

    return summary


def generate_questions(skills, projects):

    prompt = f"""
You are an expert AI technical interviewer.

Generate a structured interview question list.

Candidate Skills:
{skills}

Projects:
{projects}

Follow this format strictly:

SECTION 1: Basic HR / Behavioral Questions
Generate 5 questions including:
- Introduce yourself
- Strengths and weaknesses
- Career goals

SECTION 2: Technical Questions (Skill Based)
For EACH skill listed, generate possible important interview questions.

SECTION 3: Coding Questions
Generate 5 coding problems related to Python / Data Science.
Include simple to intermediate difficulty suitable for freshers.

SECTION 4: Project Based Questions
Generate 5 questions asking about project explanation, design choices, model selection, and improvements,why this why not others.

SECTION 5: Scenario / Problem Solving Questions
Generate 3 real-world questions like debugging, optimization, deployment.

Return in clean numbered format with section headings.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def generate_resume_tips(details, matched, missing, resume_text):

    prompt = f"""
You are an expert career coach.

Analyze the candidate resume and give ONLY 4-5 short bullet points.

Rules:
• Each tip must be one line only
• No long sentences
• Keep it simple
. Limit to max 3–4 points only  

Candidate Details:
Name: {details.get("name")}
Education: {details.get("education")}
Experience: {details.get("experience")}

Matched Skills:
{matched}

Missing Skills:
{missing}

Resume Content:
{resume_text[:1500]}

Return format:

• Tip 1
• Tip 2
• Tip 3
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        tips = response.choices[0].message.content

    except:
        tips = "• Unable to generate tips"

    return tips


def generate_career_roadmap(details, matched, missing):

    prompt = f"""
You are an AI career mentor.

Create a SHORT step-by-step career roadmap (4 steps max).

Rules:
• Each step must be ONE LINE only, Don't give each point more content.each point should be short and crisp
• Keep it practical and beginner-friendly
• Focus on getting a job
. Limit to max 3–4 points only



Candidate:
Education: {details.get("education")}
Experience: {details.get("experience")}

Matched Skills:
{matched}

Missing Skills:
{missing}

Return format:

1. Step 1
2. Step 2
3. Step 3
4. Step 4
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        roadmap = response.choices[0].message.content

    except:
        roadmap = "Career roadmap could not be generated."

    return roadmap


# ---------------- HOME PAGE ---------------- #

@app.route("/")
def home():
    return render_template("home.html")


# ---------------- RECRUITER PAGE ---------------- #

@app.route("/recruiter", methods=["GET", "POST"])
def recruiter():

    global matched   # for interview question generation

    if request.method == "POST":

        file = request.files["resume"]
        jd = request.form["jd"]

        resume_text = extract_text_from_pdf(file)
        details = extract_details(resume_text)

        skill_percent, matched, missing = skill_match(resume_text, jd)
        education_percent = education_score(details["education"], jd)
        exp_percent = experience_score(details["years"], jd)

        overall, label = overall_score(skill_percent, education_percent, exp_percent)

        
        summary = generate_candidate_summary(details, matched, missing)

        return render_template( 
            "recruiter.html",
            details=details,
            skill_percent=skill_percent,
            education=education_percent,
            experience=exp_percent,
            overall=overall,
            label=label,
            matched=matched,
            missing=missing,
            summary=summary,
        )

    return render_template("recruiter.html")


# ---------------- DOWNLOAD QUESTIONS PDF ---------------- #

@app.route("/download_questions")
def download_questions():

    questions = generate_questions(matched, [])

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(200,10,"AI Generated Interview Questions", ln=True)

    for line in questions.split("\n"):
        pdf.multi_cell(0,10,line)

    file_name = "interview_questions.pdf"
    pdf.output(file_name)

    return send_file(file_name, as_attachment=True)


# ---------------- CANDIDATE PAGE ---------------- #

@app.route("/candidate", methods=["GET","POST"])
def candidate():

    if request.method == "POST":

        file = request.files["resume"]
        jd = request.form["jd"]

        resume_text = extract_text_from_pdf(file)
        details = extract_details(resume_text)

        skill_percent, matched, missing = skill_match(resume_text, jd)
        education_percent = education_score(details["education"], jd)
        exp_percent = experience_score(details["years"], jd)

        overall, label = overall_score(skill_percent, education_percent, exp_percent)

        summary = generate_candidate_summary(details, matched, missing)

         # ✅ AI Resume Tips 
        tips = generate_resume_tips(details, matched, missing, resume_text)

        roadmap = generate_career_roadmap(details, matched, missing)

        return render_template(
            "candidate.html",
            details=details,
            overall=overall,
            label=label,
            matched=matched,
            missing=missing,
            tips=tips,
            summary=summary,
            roadmap=roadmap,
        )

    return render_template("candidate.html")


# ---------------- PDF TEXT EXTRACTION ---------------- #

def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text


# ---------------- EXTRACT DETAILS ---------------- #

def extract_details(text):

    lines = text.split("\n")

    email_match = re.search(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text
    )
    email = email_match.group(0) if email_match else "Not Found"

    phone_match = re.search(r'\b\d{10}\b', text)
    phone = phone_match.group(0) if phone_match else "Not Found"

    name = "Not Found"

    for line in lines[:10]:

        line = line.strip()

        if "@" in line or any(char.isdigit() for char in line):
            continue

        clean = re.sub(r'[^A-Za-z\s]', '', line).strip()

        words = clean.split()

        if 2 <= len(words) <= 4:

            words = [w for w in words if w[0].isupper()]

            if len(words) >= 2:
                name = " ".join(words[-2:]).title()
                break

    education = "Not Found"

    degree_keywords = [
        "b.tech", "b.e", "m.tech", "mba",
        "bsc", "msc", "bachelor", "master"
    ]

    for line in lines:
        if any(deg in line.lower() for deg in degree_keywords):
            education = line
            break

    years = 0
    experience = "Fresher"

    exp_match = re.search(r'(\d+)\+?\s*(years|year)', text.lower())

    if exp_match:
        years = int(exp_match.group(1))
        experience = f"{years} Years Experience"

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "education": education,
        "experience": experience,
        "years": years
    }


# ---------------- SKILL MATCH ---------------- #

def skill_match(resume_text, jd_text):

    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    matched = []
    missing = []
    jd_skills = []

    for skill in TECHNICAL_SKILLS:

        pattern = r'\b' + re.escape(skill.lower()) + r'\b'

        if re.search(pattern, jd_text):

            jd_skills.append(skill)

            if re.search(pattern, resume_text):
                matched.append(skill)
            else:
                missing.append(skill)

    percent = int((len(matched) / len(jd_skills)) * 100) if jd_skills else 0

    return percent, matched, missing


# ---------------- EDUCATION SCORE ---------------- #

def education_score(candidate_edu, jd_text):

    jd_text = jd_text.lower()

    if candidate_edu == "Not Found":
        return 50

    if "b.tech" in jd_text or "b.e" in jd_text or "bachelor" in jd_text:

        if "b.tech" in candidate_edu.lower() or "b.e" in candidate_edu.lower():
            return 100
        else:
            return 70

    return 80


# ---------------- EXPERIENCE SCORE ---------------- #

def experience_score(candidate_years, jd_text):

    jd_text = jd_text.lower()

    match = re.search(r'(\d+)-(\d+)\s*years', jd_text)

    if match:
        min_exp = int(match.group(1))
        max_exp = int(match.group(2))
    else:
        return 80

    if min_exp <= candidate_years <= max_exp:
        return 100
    elif candidate_years < min_exp:
        return 70
    else:
        return 85


# ---------------- OVERALL SCORE ---------------- #

def overall_score(skill_percent, education_percent, experience_percent):

    overall = int((skill_percent + education_percent + experience_percent) / 3)

    if overall >= 80:
        label = "✅ Good Fit"
    elif overall >= 60:
        label = "⚠️ Average Fit"
    else:
        label = "❌ Poor Fit"

    return overall, label


# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)