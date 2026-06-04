import pandas as pd
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")

GOOD_KEYWORDS = [
    ".net",
    "c#",
    "asp.net",
    "angular",
    "typescript",
    "sql server",
    "azure devops",
    "ci/cd",
    "software engineer",
    "full stack",
    "web application",
    "dashboard"
]

BAD_KEYWORDS = [
    "intern",
    "fresh graduate",
    "sales",
    "commission only",
    "php only",
    "wordpress only"
]

def score_job(row):
    text = " ".join(str(row.get(col, "")) for col in row.index).lower()

    score = 0
    matched = []

    for keyword in GOOD_KEYWORDS:
        if keyword in text:
            score += 1
            matched.append(keyword)

    for keyword in BAD_KEYWORDS:
        if keyword in text:
            score -= 2

    score = max(1, min(10, score))

    if score >= 7:
        recommendation = "Apply"
    elif score >= 4:
        recommendation = "Maybe"
    else:
        recommendation = "Skip"

    reason = f"Matched skills: {', '.join(matched) if matched else 'No strong match found'}"

    return pd.Series({
        "Match Score": score,
        "Recommendation": recommendation,
        "Reason": reason
    })

today = datetime.now().strftime("%Y-%m-%d")
input_path = DATA_DIR / f"jobs_{today}.csv"
output_path = DATA_DIR / f"ranked_jobs_{today}.xlsx"

df = pd.read_csv(input_path)
ranking = df.apply(score_job, axis=1)
df = pd.concat([df, ranking], axis=1)

df = df.sort_values(by="Match Score", ascending=False)
df.to_excel(output_path, index=False)

print(f"Ranked jobs saved to {output_path}")
