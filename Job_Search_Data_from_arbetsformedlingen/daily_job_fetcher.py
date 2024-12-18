import requests
import pandas as pd
import schedule
import time
from datetime import datetime
import os
import webbrowser
import subprocess

# --- Configuration ---
API_URL = "https://jobsearch.api.jobtechdev.se/search"
HEADERS = {"accept": "application/json"}
MUNICIPALITY_CODE = "1480"  # Göteborg municipality code
OCCUPATION_FIELD = "apaJ_2ja_LuF"  # Data/IT field ID from Taxonomy API
SEARCH_QUERY = "software developer OR software engineer OR IT OR mjukvaruingenjör OR utvecklare"
NON_CONSULTANCY_COMPANIES = [
    "Gotit", "Volvo Car Corporation", "Mullvad VPN", "Trafikverket", "Skatteverket",
    "Jeppesen", "Hogia HR Systems AB", "Hogia Infrastructure Products AB", "Hogia Facility Management AB",
    "Hogia Business Products AB", "deepNumbers systems AB", "Åre Kommun", "Provide IT Sweden AB", "Acoem AB",
    "Icomera AB", "Volvo Group", "Drakryggen", "Saab AB", "Qamcom", "Humly", "Compary AB", "Assemblin",
    "QRTECH", "Novacura", "NOVENTUS SYSTEMS AKTIEBOLAG", "Polismyndigheten", "SOLTAK AB", "Göteborg Energi",
    "Vipas AB", "HaleyTek AB", "Zacco Digital Trust", "Autocom", "Benify", "Logikfabriken AB", "DENTSPLY IH AB"
]
OUTPUT_FILE = "filtered_jobs_gothenburg.csv"
HTML_FILE = "index.html"

# --- Functions ---
def fetch_jobs(query, municipality, occupation_field, limit=50):
    print(f"[{datetime.now()}] Fetching job data...")
    params = {"q": query, "municipality": municipality, "occupation-field": occupation_field, "limit": limit}
    response = requests.get(API_URL, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        print(f"Fetched {len(response.json().get('hits', []))} jobs.")
        return response.json().get("hits", [])
    else:
        print(f"Error: Unable to fetch data. Status Code {response.status_code}")
        return []

def filter_and_categorize_jobs(jobs):
    print(f"[{datetime.now()}] Filtering and categorizing jobs...")
    categorized_jobs = []

    for job in jobs:
        employer = job.get("employer", {}).get("name", "").strip()
        description = job.get("description", {}).get("text", "").lower()
        headline = job.get("headline", "").strip()
        publication_date = job.get("publication_date", "")
        job_link = job.get("webpage_url", "")
        
        if employer in NON_CONSULTANCY_COMPANIES:
            category = "Non-Consultancy"
        elif "consult" in description or "advisory" in description:
            category = "Consultancy"
        elif "developer" in description or "engineer" in description:
            category = "IT Developer"
        else:
            category = "Uncategorized"
        
        categorized_jobs.append({
            "Title": headline,
            "Employer": employer,
            "Category": category,
            "Publication Date": publication_date,
            "Job Link": job_link
        })
    
    return categorized_jobs

def save_to_csv(jobs, filename):
    print(f"[{datetime.now()}] Saving jobs to {filename}...")
    pd.DataFrame(jobs).to_csv(filename, index=False)
    print(f"Saved {len(jobs)} jobs to {filename}.")

def save_to_html(jobs, filename):
    print(f"[{datetime.now()}] Saving jobs to {filename}...")
    html_content = """
    <html>
    <head>
        <title>Job Listings</title>
        <style>
            table {width: 90%; margin: 20px auto; border-collapse: collapse;}
            th, td {border: 1px solid #ddd; padding: 8px; text-align: left;}
            th {background-color: #4CAF50; color: white;}
            tr:nth-child(even) {background-color: #f2f2f2;}
        </style>
    </head>
    <body>
        <h1 style="text-align:center;">Job Listings</h1>
        <table>
            <tr>
                <th>Title</th><th>Employer</th><th>Category</th><th>Publication Date</th><th>Job Link</th>
            </tr>
    """
    for job in jobs:
        html_content += f"""
            <tr>
                <td>{job['Title']}</td>
                <td>{job['Employer']}</td>
                <td>{job['Category']}</td>
                <td>{job['Publication Date']}</td>
                <td><a href="{job['Job Link']}" target="_blank">View Job</a></td>
            </tr>
        """
    html_content += "</table></body></html>"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"Saved HTML file: {filename}")

def deploy_to_firebase():
    print(f"[{datetime.now()}] Deploying updated HTML to Firebase...")
    try:
        subprocess.run(["firebase", "deploy"], check=True)
        print("Deployment successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error during deployment: {e}")

def job_scheduler():
    jobs = fetch_jobs(SEARCH_QUERY, MUNICIPALITY_CODE, OCCUPATION_FIELD)
    filtered_jobs = filter_and_categorize_jobs(jobs)
    save_to_csv(filtered_jobs, OUTPUT_FILE)
    save_to_html(filtered_jobs, HTML_FILE)
    deploy_to_firebase()

# --- Scheduling ---
print("Job Scheduler started... Press Ctrl+C to stop.")
schedule.every().day.at("08:00").do(job_scheduler)

# Initial Run
job_scheduler()

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
