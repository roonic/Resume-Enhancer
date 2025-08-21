import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

SHARPAPI_KEY = os.getenv("SHARPAPI_KEY")
SUBMIT_URL = "https://api.apyhub.com/sharpapi/api/v1/hr/resume_job_match_score"

def submit_job(resume_path, job_description, language="en"):
    """
    Submit resume + job description to SharpAPI and return the status_url.
    """
    headers = {
        "apy-token": SHARPAPI_KEY,
        "Accept": "application/json"
    }

    print(f"[DEBUG] Submitting resume: {resume_path}")
    with open(resume_path, "rb") as resume_file:
        files = {
            "file": resume_file,
            "content": (None, job_description),
            "language": (None, language)
        }
        response = requests.post(SUBMIT_URL, headers=headers, files=files)
    
    print(f"[DEBUG] Submit response status: {response.status_code}")
    response.raise_for_status()
    data = response.json()
    print(f"[DEBUG] Submit response JSON: {data}")
    
    status_url = data.get("status_url")
    print(f"[DEBUG] Status URL: {status_url}")
    return status_url

def poll_results(status_url, interval=5, timeout=60):
    """
    Poll the status_url until results are ready or timeout is reached.
    Returns JSON result or None if timeout.
    """
    headers = {"apy-token": SHARPAPI_KEY}
    elapsed = 0
    print(f"[DEBUG] Start polling ATS results at: {status_url}")
    while elapsed < timeout:
        response = requests.get(status_url, headers=headers)
        print(f"[DEBUG] Polling response status: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        if "match_scores" in data:
            print("[DEBUG] ATS results ready")
            return data
        time.sleep(interval)
        elapsed += interval
        print(f"[DEBUG] Waiting... elapsed: {elapsed}s")
    
    print("[DEBUG] Polling timeout reached")
    return None

def get_ats_score(resume_path, job_description, language="en", interval=5, timeout=60):
    """
    Wrapper: submit job + poll results.
    """
    status_url = submit_job(resume_path, job_description, language)
    if not status_url:
        print("[DEBUG] No status URL returned from submit")
        return None
    #return poll_results(status_url, interval, timeout)
    return
