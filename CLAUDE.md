
# Project Instructions

## Project
This repo is a GitHub Actions based job hunter agent.

## Goal
Every morning, search for suitable Malaysia software jobs, rank them, save the results, and notify me on Telegram.

## Tech Stack
- Python 3.11
- GitHub Actions
- pandas
- openpyxl
- requests
- BeautifulSoup if needed
- Telegram Bot API

## Rules
- Do not commit secrets.
- Do not hardcode Telegram token, chat ID, API keys, passwords, cookies, or session tokens.
- Use GitHub Secrets for sensitive values.
- Do not auto-apply to jobs.
- Do not invent job data.
- Respect website terms.
- Avoid aggressive scraping.
- Add delay between requests.
- If one source fails, continue with other sources.
- Keep scraper code modular.

## Target Roles
- .NET Developer
- C# Developer
- Angular Developer
- Full Stack Developer
- Software Engineer
- AI Engineer

## Target Locations
- Kuala Lumpur
- Selangor
- Remote Malaysia

## Output Files
Save results to:
- data/jobs_YYYY-MM-DD.csv
- data/jobs_YYYY-MM-DD.xlsx
- data/ranked_jobs_YYYY-MM-DD.xlsx

## Telegram Summary
Telegram message should include:
- total jobs found
- total Apply
- total Maybe
- top 10 jobs
- title
- company
- location
- salary
- match score
- recommendation
- reason
- URL
