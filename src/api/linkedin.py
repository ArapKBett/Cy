import requests
from bs4 import BeautifulSoup
import uuid
import time
from src.utils.logger import setup_logger

logger = setup_logger()

def scrape_linkedin_jobs():
    jobs = []
    # Search for cybersecurity jobs worldwide
    url = "https://www.linkedin.com/jobs/search/?keywords=cybersecurity"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        job_cards = soup.select(".jobs-search__results-list > li")
        for card in job_cards[:5]:  # Limit to 5 jobs to avoid rate limits
            title_elem = card.select_one(".base-search-card__title")
            company_elem = card.select_one(".base-search-card__subtitle")
            location_elem = card.select_one(".job-search-card__location")
            link_elem = card.select_one("a.base-card__full-link")
            
            if title_elem and company_elem and link_elem:
                job = {
                    "id": str(uuid.uuid4()),
                    "title": title_elem.text.strip(),
                    "company": company_elem.text.strip(),
                    "location": location_elem.text.strip() if location_elem else "N/A",
                    "url": link_elem["href"].split("?")[0],  # Clean URL
                    "platform": "LinkedIn"
                }
                jobs.append(job)
                logger.info(f"Scraped job: {job['title']} from LinkedIn")
                time.sleep(1)  # Avoid rate limiting
    except Exception as e:
        logger.error(f"Error scraping LinkedIn: {e}")
        logger.info("Consider using Selenium for JavaScript-rendered content or LinkedIn API if available.")
    
    return jobs

# Optional: If LinkedIn blocks scraping, use Selenium (uncomment and configure)
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_linkedin_jobs_selenium():
    jobs = []
    url = "https://www.linkedin.com/jobs/search/?keywords=cybersecurity"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(3)  # Wait for page to load
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        job_cards = soup.select(".jobs-search__results-list > li")
        for card in job_cards[:5]:
            title_elem = card.select_one(".base-search-card__title")
            company_elem = card.select_one(".base-search-card__subtitle")
            location_elem = card.select_one(".job-search-card__location")
            link_elem = card.select_one("a.base-card__full-link")
            
            if title_elem and company_elem and link_elem:
                job = {
                    "id": str(uuid.uuid4()),
                    "title": title_elem.text.strip(),
                    "company": company_elem.text.strip(),
                    "location": location_elem.text.strip() if location_elem else "N/A",
                    "url": link_elem["href"].split("?")[0],
                    "platform": "LinkedIn"
                }
                jobs.append(job)
                logger.info(f"Scraped job: {job['title']} from LinkedIn (Selenium)")
    except Exception as e:
        logger.error(f"Error scraping LinkedIn with Selenium: {e}")
    finally:
        driver.quit()
    
    return jobs
"""
