from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Keeping your ChromeDriver path as it is
CHROMEDRIVER_PATH = "./chromedriver.exe"

def scrap_website(website):
    """Scrapes the given website and extracts the DOM body content."""
    print("🟡 Launching Chrome Browser...")

    options = Options()
    options.add_argument("--headless")  # Run without UI
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

    try:
        driver.get(website)
        print("🟢 Page Loaded Successfully")

        time.sleep(3)  # Wait for content to fully load
        html = driver.page_source  # Fetch the full HTML

        return extract_body_content(html)  # Extract only the meaningful content
    finally:
        driver.quit()  # Ensure browser closes properly


def extract_body_content(html_content):
    """Extracts and cleans the body content from HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body

    return str(body_content) if body_content else ""


def clean_body_content(body_content):
    """Removes unnecessary elements and formats the extracted DOM structure."""
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove scripts and styles for cleaner parsing
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    cleaned_content = soup.get_text(separator="\n")  # Ensure structured text
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    """Splits DOM content into chunks to fit into LLM input limits."""
    return [dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)]
