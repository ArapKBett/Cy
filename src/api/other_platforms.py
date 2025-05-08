import requests
from bs4 import BeautifulSoup
import uuid
import time
from src.utils.logger import setup_logger

logger = setup_logger()

def scrape_ziprecruiter_jobs():
    jobs = []
    # Search for cybersecurity jobs worldwide
    url = "https://www.ziprecruiter.com/jobs-search?search=cybersecurity"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        job_cards = soup.select(".job_content")
        for card in job_cards[:5]:  # Limit to 5 jobs to avoid rate limits
            title_elem = card.select_one(".job_title")
            company_elem = card.select_one(".hiring_company_text")
            location_elem = card.select_one(".job_location")
            link_elem = card.select_one("a.job_link")
            
            if title_elem and company_elem and link_elem:
                job = {
                    "id": str(uuid.uuid4()),
                    "title": title_elem.text.strip(),
                    "company": company_elem.text.strip(),
                    "location": location_elem.text.strip() if location_elem else "N/A",
                    "url": link_elem["href"],
                    "platform": "ZipRecruiter"
                }
                jobs.append(job)
                logger.info(f"Scraped job: {job['title']} from ZipRecruiter")
                time.sleep(1)  # Avoid rate limiting
    except Exception as e:
        logger.error(f"Error scraping ZipRecruiter: {e}")
        logger.info("Consider using Selenium for JavaScript-rendered content.")
    
    return jobs

# Optional: Selenium fallback for ZipRecruiter
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_ziprecruiter_jobs_selenium():
    jobs = []
    url = "https://www.ziprecruiter.com/jobs-search?search=cybersecurity"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(3)  # Wait for page to load
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        job_cards = soup.select(".job_content")
        for card in job_cards[:5]:
            title_elem = card.select_one(".job_title")
            company_elem = card.select_one(".hiring_company_text")
            location_elem = card.select_one(".job_location")
            link_elem = card.select_one("a.job_link")
            
            if title_elem and company_elem and link_elem:
                job = {
                    "id": str(uuid.uuid4()),
                    "title": title_elem.text.strip(),
                    "company": company_elem.text.strip(),
                    "location": location_elem.text.strip() if location_elem else "N/A",
                    "url": link_elem["href"],
                    "platform": "ZipRecruiter"
                }
                jobs.append(job)
                logger.info(f"Scraped job: {job['title']} from ZipRecruiter (Selenium)")
    except Exception as e:
        logger.error(f"Error scraping ZipRecruiter with Selenium: {e}")
    finally:
        driver.quit()
    
    return jobs
"""
