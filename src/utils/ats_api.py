import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHARPAPI_KEY = os.getenv("SHARPAPI_KEY")
SHARPAPI_URL = "https://api.apyhub.com/utility/sharpapi-resume-job-match-score"

def get_ats_score(resume_text, job_description_text):
    headers = {
        "apy-token": SHARPAPI_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "resume": resume_text,
        "jobDescription": job_description_text
    }
    try:
        response = requests.post(SHARPAPI_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling SharpAPI: {e}")
        return None


