"""
Score Calculator: Computes a match score between a resume and a job description using semantic similarity, then generates LLM reasoning to explain the score.
"""

import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from prompts.templates import MATCH_SCORE_REASONING_PROMPT

load_dotenv()

class MatchScoreResult(BaseModel):
    match_score: float
    reasoning: str

def calculate_match_score(resume_text: str, job_description: str) -> MatchScoreResult:
    """
    Calculate a match score between a resume and a job description using embedding similarity, then generate LLM reasoning to explain it.
    
    Args:
        resume_text: Plain text extracted from the resume.
        job_description: Plain text extracted from the job description.

    Returns:
        MatchScoreResult: A structured object containing the match score and reasoning.
    """

    embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    resume_embedding = embed_model.encode([resume_text])
    job_embedding = embed_model.encode([job_description])
    similarity_score = cosine_similarity(resume_embedding, job_embedding)[0][0]
    similarity_score = round(float(similarity_score) * 100, 2)

    prompt = MATCH_SCORE_REASONING_PROMPT.format(resume_text=resume_text, job_description=job_description, similarity_score=similarity_score)

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": MatchScoreResult,
        }
    )

    return MatchScoreResult.model_validate_json(response.text)

#Code for unit testing the function
if __name__ == "__main__":
    sample_resume = "Experienced in Python, SQL, Git, and basic machine learning with scikit-learn."
    sample_jd = "Looking for a candidate skilled in Python, PyTorch, Docker, and cloud deployment (AWS/GCP)."
    
    result = calculate_match_score(sample_resume, sample_jd)
    print(result.model_dump_json(indent=2))