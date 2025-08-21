import json
import os
import time
import google.generativeai as genai
from google.generativeai.types import generation_types

# API key should be injected at runtime (e.g., in Canvas environment)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)


def call_gemini_api(prompt, model_name="gemini-2.5-flash-preview-05-20",
                    json_output=False, generation_config=None, chat_history=None):
    """
    Helper function to call the Gemini API with exponential backoff.
    Supports JSON output when json_output=True.
    """
    chat_history = chat_history or []
    model = genai.GenerativeModel(model_name)

    # Default schema if JSON output is expected but not provided
    if json_output and generation_config is None:
        generation_config = {"response_mime_type": "application/json"}

    retries, max_retries, base_delay = 0, 5, 1

    while retries < max_retries:
        try:
            response = model.generate_content(prompt, generation_config=generation_config)

            if json_output:
                json_text = getattr(response, "text", None)
                if not json_text:
                    return None

                cleaned = json_text.strip().strip("`")
                try:
                    return json.loads(cleaned)
                except json.JSONDecodeError as e:
                    print(f"JSON decoding error: {e}, Raw response: {cleaned}")
                    return None
            return getattr(response, "text", None)

        except (generation_types.BlockedPromptException,
                generation_types.StopCandidateException) as e:
            print(f"Prompt blocked/stopped: {e}")
            return None
        except Exception as e:
            error_message = str(e).lower()
            if "rate limit" in error_message or "resource exhausted" in error_message:
                delay = base_delay * (2 ** retries)
                print(f"Rate limit hit. Retrying in {delay}s...")
                time.sleep(delay)
                retries += 1
            else:
                print(f"Unexpected API error: {e}")
                return None

    print(f"Max retries ({max_retries}) exceeded.")
    return None


def get_ats_score(resume_text, job_description_text):
    prompt = f"""
You are an ATS scoring expert. Given the resume and job description below,
analyze how well the candidate matches the job.
Return a JSON with:
- overall_match (0-100)
- skills_match (0-100)
- experience_match (0-100)
- education_match (0-100)
- explanations: detailed reasoning for each score

Resume:
{resume_text}

Job Description:
{job_description_text}
"""
    try:
        result = call_gemini_api(prompt, json_output=True)
        return result if isinstance(result, dict) else None
    except Exception as e:
        print(f"Error calling Gemini API for ATS scoring: {e}")
        return None


def get_suggestions(resume_text, job_description_text, ats_result):
    """
    Generates structured suggestions for improving a resume.
    """
    prompt = f"""
You are a career coach and resume expert. Given the resume, job description,
and ATS result, provide structured JSON suggestions.

Keys:
- missing_skills
- emphasize_skills
- section_reorganization
- other_recommendations

Resume:
{resume_text}

Job Description:
{job_description_text}

ATS Result:
{json.dumps(ats_result)}
"""
    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "object",
            "properties": {
                "missing_skills": {"type": "array", "items": {"type": "string"}},
                "emphasize_skills": {"type": "array", "items": {"type": "string"}},
                "section_reorganization": {"type": "array", "items": {"type": "string"}},
                "other_recommendations": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["missing_skills", "emphasize_skills", "section_reorganization", "other_recommendations"]
        }
    }

    raw_response = call_gemini_api(prompt, json_output=True, generation_config=generation_config)
    return raw_response or {
        "missing_skills": [],
        "emphasize_skills": [],
        "section_reorganization": [],
        "other_recommendations": []
    }


def generate_enhanced_resume(resume_text, job_description_text, ats_result, suggestions):
    """
    Generates an ATS-optimized, job-relevant resume in structured JSON format.
    Ensures experience and education are arrays of objects for PDF/HTML rendering.
    """
    prompt = f"""
You are an expert resume writer. Rewrite the resume into an ATS-optimized, job-relevant single-page version.

Requirements:
- Sections: Summary, Skills, Experience, Education, Selected Projects
- Highlight relevant experience/skills
- Incorporate missing skills (without adding false info)
- Apply ATS suggestions
- Concise, readable, single-page
- Use bullet points and strong action verbs
- Return strictly as valid JSON
- Experience must be an array of objects: {{ "title": "...", "company": "...", "location": "...", "duration": "...", "responsibilities": ["...", "..."] }}
- Education must be an array of objects: {{ "degree": "...", "institution": "...", "graduation_year": "..." }}

Original Resume:
{resume_text}

Job Description:
{job_description_text}

ATS Scoring Result:
{json.dumps(ats_result)}

Suggestions:
{json.dumps(suggestions)}
"""

    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "contact_info": {"type": "string"},
                "summary": {"type": "string"},
                "skills": {"type": "array", "items": {"type": "string"}},
                "experience": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "company": {"type": "string"},
                            "location": {"type": "string"},
                            "duration": {"type": "string"},
                            "responsibilities": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["title", "company", "location", "duration", "responsibilities"]
                    }
                },
                "education": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "degree": {"type": "string"},
                            "institution": {"type": "string"},
                            "graduation_year": {"type": "string"}
                        },
                        "required": ["degree", "institution", "graduation_year"]
                    }
                },
                "selected_projects": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["name", "contact_info", "summary", "skills", "experience", "education", "selected_projects"]
        }
    }

    try:
        raw_response = call_gemini_api(prompt, json_output=True, generation_config=generation_config)
        return raw_response if isinstance(raw_response, dict) else None
    except Exception as e:
        print(f"Error generating enhanced resume: {e}")
        return None
