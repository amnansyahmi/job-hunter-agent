import pandas as pd
from datetime import datetime

# First version: manually add/search from simpler sources.
# Later you can replace this with Playwright scraping logic.

jobs = [
    {
        "Job Title": ".NET Developer",
        "Company Name": "Example Company",
        "Location": "Kuala Lumpur",
        "Salary Range": "RM 7,000 - RM 10,000",
        "Key Skills": ".NET, C#, SQL, Angular",
        "Date Posted": "Today",
        "Job URL": "https://example.com/job",
        "Description": "Develop web applications using .NET and Angular."
    }
]

df = pd.DataFrame(jobs)

today = datetime.now().strftime("%Y-%m-%d")
output_path = f"data/jobs_{today}.xlsx"

df.to_excel(output_path, index=False)

print(f"Saved {len(df)} jobs to {output_path}")
