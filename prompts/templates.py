"""
Prompt Templates: This module is a centralized storage for all LLM prompts used in the application.
"""

SKILLS_GAP_PROMPT = """
You are an expert technical recruiter. Compare the resume uploaded against the job description and identify:
1. Skills present in the resume that match the job requirements
2. Skills required by the job description but missing from the resume

Resume:
{resume_text}

Job Description:
{job_description}

Provide your analysis with clear reasoning for your assessment.
"""

MATCH_SCORE_REASONING_PROMPT = """
You are reviewing how well a candidate's resume aligns with a job description. A numerical similarity score has already been calculated for the given resume and job description : {similarity_score}/100

Resume:
{resume_text}

Job Description:
{job_description}

Explain in 2-5 sentences why this score makes sense, referencing specific overlapping or missing qualifications.
"""

RESUME_REWRITE_PROMPT = """
You are an expert resume writer. Rewrite the resume uploaded to better align with the given job description, while keeping all information truthful and factually accurate to the original resume. Do not fabricate experience, skills, qualifications or any other information that are not present in the original.

STRICT RULE: You must not add any skill, technology, tool, certification, or experience that is not explicitly present in the original resume. You may only rephrase, reorganize, or emphasize what is already there. If a skill required by the job is missing from the resume, do not include it in the rewritten version.

Original Resume:
{resume_text}

Job Description:
{job_description}

Identified Skill Gaps (for context only — do not add these to the rewritten resume):
{missing_skills}

Rewrite the resume to better highlight relevant experience and naturally incorporate the candidate's existing skills in ways that align with the job requirements.
"""