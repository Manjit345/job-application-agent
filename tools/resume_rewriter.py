"""
Resume Rewriter: Rewrites a resume to better align with a job description while strictly preserving the original meaning and factual accuracy.
It does not fabricate any new information which are not present in the original resume. 
"""

import os
from dotenv import load_dotenv
from google import genai
from prompts.templates import RESUME_REWRITE_PROMPT
from tools.utils import call_with_retry

load_dotenv()

def rewrite_resume(resume_text: str, job_description: str, missing_skills:list) -> str:
    """
    Rewrite a resume which would optimize it for a specific job description.

    Args:
        resume_text: Plain text extracted from the resume.
        job_description: Plain text extracted from the target job description.
        missing_skills: A list of skills that are identified to be missing from the resume but are required in the job description.

    Returns:
        str: The rewritten resume as plain text which is optimized for the job description.
    """
    prompt = RESUME_REWRITE_PROMPT.format(resume_text=resume_text, job_description=job_description, missing_skills=", ".join(missing_skills))

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    response = call_with_retry(
        client=client,
        model="gemini-3.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "text/plain",
        }
    )
    
    return response.text.strip()

#Code for unit testing the function
if __name__ == "__main__":
    sample_resume = "Experienced in Python, SQL, Git, and basic machine learning with scikit-learn."
    sample_jd = "Looking for a candidate skilled in Python, PyTorch, Docker, and cloud deployment (AWS/GCP)."
    sample_missing_skills = ["PyTorch", "Docker", "AWS", "GCP"]

    result = rewrite_resume(sample_resume, sample_jd, sample_missing_skills)
    print(result)