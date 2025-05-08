import requests
from bs4 import BeautifulSoup
import uuid
from src.utils.logger import setup_logger

logger = setup_logger()

def scrape_indeed_jobs():
    jobs = []
    # Removed location filter to capture global jobs
    url = "https://www.indeed.com/jobs?q=cybersecurity"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        job_cards = soup.select(".jobsearch-ResultsList > li")
        for card in job_cards[:5]:  # Limit to 5 jobs to avoid rate limits
            title_elem = card.select_one(".jobTitle")
            company_elem = card.select_one(".companyName")
            location_elem = card.select_one(".companyLocation")
            link_elem = card.select_one("a[id^='job_']")
            
            if title_elem and company_elem and link_elem:
                job = {
                    "id": str(uuid.uuid4()),
                    "title": title_elem.text.strip(),
                    "company": company_elem.text.strip(),
                    "location": location_elem.text.strip() if location_elem else "N/A",
                    "url": f"https://www.indeed.com{link_elem['href']}",
                    "platform": "Indeed"
                }
                jobs.append(job)
                logger.info(f"Scraped job: {job['title']} from Indeed")
    except Exception as e:
        logger.error(f"Error scraping Indeed: {e}")
    
    return jobs
