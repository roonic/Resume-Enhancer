import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_suggestions(resume_text, job_description_text):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""Given the following resume and job description, please provide suggestions to improve the resume to be more relevant, minimal, and ATS-friendly. Reorganize the resume into the following sections: Summary, Skills, Experience, Education. Highlight missing skills from the job description and suggest how to incorporate them. Also, suggest how to make existing skills more prominent if they are relevant but not clearly stated. 

Resume:
{resume_text}

Job Description:
{job_description_text}

Provide the improved resume content in a structured format, clearly delineating each section. Also, provide a separate list of suggestions for improvement, including how to incorporate missing skills and highlight existing ones. """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None


