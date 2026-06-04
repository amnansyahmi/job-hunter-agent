import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from openai import OpenAI

DATA_DIR = Path("data")

AI_BASE_URL = os.environ["AI_BASE_URL"]
AI_API_KEY = os.environ["AI_API_KEY"]
AI_MODEL = os.environ.get("AI_MODEL", "ai-nonymauz-coding")

client = OpenAI(
    base_url=AI_BASE_URL,
    api_key=AI_API_KEY,
)

def get_latest_jobs_file():
    today = datetime.now().strftime("%Y-%m-%d")
    path = DATA_DIR / f"jobs_{today}.csv"

    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    return path

def rank_with_ai(job):
    prompt = f"""
You are ranking software jobs for a developer in Malaysia.

Candidate profile:
- C#
- .NET Framework
- .NET Core
- ASP.NET MVC
- Angular
- SQL Server
- Azure DevOps
- CI/CD
- Dashboard development
- Legacy system modernization
- Production support
- Interested in AI automation

Preferred jobs:
- .NET Developer
- C# Developer
- Angular Developer
- Full Stack Developer
- Software Engineer
- AI Engineer

Preferred location:
- Kuala Lumpur
- Selangor
- Remote Malaysia

Avoid:
- Internship
- Fresh graduate only
- Pure sales
- Commission-only
- Jobs that require fake experience

Job:
Title: {job.get("Job Title", "")}
Company: {job.get("Company Name", "")}
Location: {job.get("Location", "")}
Salary: {job.get("Salary Range", "")}
Skills: {job.get("Key Skills", "")}
Description: {job.get("Description", "")}
URL: {job.get("Job URL", "")}

Return only valid JSON with this structure:
{{
  "match_score": 1,
  "recommendation": "Apply",
  "reason": "short reason",
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1"]
}}

Rules:
- match_score must be from 1 to 10.
- recommendation must be one of: Apply, Maybe, Skip.
- Do not invent experience.
- Be strict but fair.
"""

    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a strict job matching assistant. Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=500,
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "match_score": 1,
            "recommendation": "Maybe",
            "reason": f"AI returned invalid JSON: {content[:200]}",
            "matched_skills": [],
            "missing_skills": []
        }

def main():
    input_path = get_latest_jobs_file()
    df = pd.read_csv(input_path)

    results = []

    for _, row in df.iterrows():
        job = row.to_dict()

        try:
            ai_result = rank_with_ai(job)
        except Exception as e:
            ai_result = {
                "match_score": 1,
                "recommendation": "Maybe",
                "reason": f"AI ranking failed: {str(e)}",
                "matched_skills": [],
                "missing_skills": []
            }

        results.append(ai_result)

    df["Match Score"] = [r.get("match_score", 1) for r in results]
    df["Recommendation"] = [r.get("recommendation", "Maybe") for r in results]
    df["Reason"] = [r.get("reason", "") for r in results]
    df["Matched Skills"] = [", ".join(r.get("matched_skills", [])) for r in results]
    df["Missing Skills"] = [", ".join(r.get("missing_skills", [])) for r in results]

    df = df.sort_values(by="Match Score", ascending=False)

    today = datetime.now().strftime("%Y-%m-%d")
    output_path = DATA_DIR / f"ranked_jobs_{today}.xlsx"
    df.to_excel(output_path, index=False)

    print(f"AI ranked jobs saved to {output_path}")

if __name__ == "__main__":
    main()
