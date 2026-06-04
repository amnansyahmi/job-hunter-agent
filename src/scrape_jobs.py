import pandas as pd
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Version 1 sample data.
# Later you replace this with real scraping logic.
jobs = [
    {
        "Job Title": ".NET Developer",
        "Company Name": "Example Company",
        "Location": "Kuala Lumpur",
        "Salary Range": "RM 7000 - RM 10000",
        "Key Skills": ".NET, C#, SQL Server, Angular",
        "Date Posted": "Today",
        "Job URL": "https://example.com/job",
        "Source": "Example",
        "Description": "Develop and maintain web applications using .NET, C#, SQL Server and Angular."
    },
    {
        "Job Title": "Angular Developer",
        "Company Name": "Another Company",
        "Location": "Selangor",
        "Salary Range": "Not disclosed",
        "Key Skills": "Angular, TypeScript, REST API",
        "Date Posted": "Today",
        "Job URL": "https://example.com/angular-job",
        "Source": "Example",
        "Description": "Build frontend dashboard features using Angular and REST APIs."
    }
]

df = pd.DataFrame(jobs)

today = datetime.now().strftime("%Y-%m-%d")
csv_path = DATA_DIR / f"jobs_{today}.csv"
xlsx_path = DATA_DIR / f"jobs_{today}.xlsx"

df.to_csv(csv_path, index=False)
df.to_excel(xlsx_path, index=False)

print(f"Saved {len(df)} jobs")
print(csv_path)
print(xlsx_path)
