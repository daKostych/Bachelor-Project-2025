from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from src.config import CHROMEDRIVER_PATH
import time
import requests
import fitz
#=======================================================================================================================
def extract_blog_text(blog=None, url_blog=None, author_blog=None, claps=None, comments=None):
    """Extracts only the blog text with titles and subtitles from Medium"""

    if blog:
        url_blog = blog.url_blog
        author_blog = blog.author_blog
        claps = blog.claps
        comments = blog.comments
    elif url_blog is None or author_blog is None or claps is None or comments is None:
        return None

    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Set User-Agent to mimic a real browser
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.119 Safari/537.36"
    )

    # Initialize WebDriver
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url_blog)
        time.sleep(5)  # Wait for page to load

        # Extract the main article element
        article = driver.find_element(By.TAG_NAME, "article")
        article_elements = article.find_elements(By.XPATH, ".//h1 | .//h2 | .//h3 | .//p | .//li")

        skip_phrases = ["follow", f"{author_blog.lower()}", f"{int(claps)}", f"{int(comments)}"]

        # Build a clean, structured text
        full_text = ""
        for elem in article_elements:
            tag_name = elem.tag_name
            text = elem.text.strip()

            if text:
                if tag_name == "h1":
                    full_text += f"\n# {text}\n"
                elif tag_name == "h2":
                    full_text += f"\n## {text}\n"
                elif tag_name == "h3":
                    full_text += f"\n### {text}\n"
                elif tag_name == "li":
                    full_text += f"    * {text}\n"
                elif tag_name == "p" and text.lower() not in skip_phrases:
                    full_text += f"{text}\n"

    except Exception as e:
        full_text = f"Error: {e}"

    finally:
        driver.quit()  # Close the browser

    return full_text.strip()
#=======================================================================================================================
def extract_paper_text(pdf_url):
    """Download PDF and extract text"""
    try:
        response = requests.get(pdf_url)
        pdf_path = "../tmp/temp_paper.pdf"

        # Save PDF
        with open(pdf_path, "wb") as f:
            f.write(response.content)

        # Open PDF and extract text
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text() for page in doc])

        return text
    except Exception as e:
        return f"Error: {e}"
#=======================================================================================================================