from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from telegram import Bot
import asyncio
import csv
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Ensure required environment variables exist
telegram_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")

if not telegram_token or not chat_id:
    raise ValueError("Telegram token or chat ID not found. Check .env file.")

bot = Bot(token=telegram_token)

# Define CSV file path dynamically
csv_file = os.path.join(os.getcwd(), "Jobs.csv")

async def send_message(job_data):
    """Send job details to Telegram."""
    message = (
        f"New Job Posted:\n\n"
        f"Title: {job_data['Title']}\n\n"
        f"Link: {job_data['Link']}\n\n"
        f"Description: {job_data['Description']}\n\n"
        f"Details: {job_data['Details']}"
    )
    print("A job sent successfully.")
    await bot.send_message(chat_id=chat_id, text=message)

def save_to_csv(job_title):
    """Save the latest job title to CSV."""
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([job_title])

def job_exists_in_csv(job_name):
    """Check if the job title already exists in CSV."""
    try:
        with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            return any(row[0] == job_name for row in reader)
    except FileNotFoundError:
        return False

async def scrape_upwork_jobs():
    """Scrape job listings from Upwork."""
    # Ensure the CSV file exists
    open(csv_file, "a").close()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    url = "https://www.upwork.com/nx/search/jobs/?nbs=1&q=scraping&sort=recency"

    # Use `with` statement to ensure the WebDriver closes properly
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the first job post to appear
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article:nth-child(1) a.up-n-link"))
            )
        except Exception as e:
            print(f"Timeout waiting for job listings: {e}")
            return

        first = True
        top_title = None

        for i in range(1, 11):  # Loop through first 10 job postings
            try:
                job = driver.find_element(By.CSS_SELECTOR, f"article:nth-child({i}) a.up-n-link")
                job_url = job.get_attribute("href")
                title = job.text.strip()

                details = driver.find_element(By.CSS_SELECTOR, f"article:nth-child({i}) ul.job-tile-info-list.text-base-sm.mb-4").text.strip() if driver.find_elements(By.CSS_SELECTOR, f"article:nth-child({i}) ul.job-tile-info-list.text-base-sm.mb-4") else ""
                description = driver.find_element(By.CSS_SELECTOR, f"article:nth-child({i}) p.mb-0.text-body-sm").text.strip() if driver.find_elements(By.CSS_SELECTOR, f"article:nth-child({i}) p.mb-0.text-body-sm") else ""

                if job_exists_in_csv(title):
                    print(f"Job '{title}' already exists in CSV. Skipping...")
                    break

                job_data = {
                    "Title": title,
                    "Link": job_url,
                    "Description": description,
                    "Details": details,
                }

                if first:
                    top_title = title
                    first = False

                await send_message(job_data)

            except Exception as e:
                print(f"Error processing job {i}: {e}")

        if top_title:
            save_to_csv(top_title)

async def main():
    """Run the job scraper."""
    await scrape_upwork_jobs()

# Run the scraper
asyncio.run(main())
