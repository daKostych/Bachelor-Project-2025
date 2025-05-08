import time
import os

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import fitz
import pandas as pd

from src.config import CHROMEDRIVER_PATH, TMP_PDF_PATH, BASE_DIR
#=======================================================================================================================
def extract_blog_text(blog=None, source="Medium", url_blog=None, author_blog=None, publisher_blog=None):
    """Extracts only the blog text with titles and subtitles from Medium/Google DeepMind"""

    if source == "Medium":
        if isinstance(blog, pd.Series):
            url_blog = blog.url_blog
            author_blog = blog.author_blog
            publisher_blog = blog.publisher_blog
        elif url_blog is None or author_blog is None or publisher_blog is None:
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
    article_elements = None

    try:
        driver.get(url_blog)
        time.sleep(5)  # Wait for page to load

        # Extract the main article element
        article = driver.find_element(By.TAG_NAME, "article")
        article_elements = None
        if source == "Medium":
            article_elements = article.find_elements(By.XPATH, ".//h1 | .//h2 | .//h3 | .//p | .//li")
        elif source == "DeepMind":
            ignore_classes = ['article-cover__eyebrow glue-label', 'article-cover__authors', 'caption', 'related-posts',
                              'glue-video__info', 'article-cover__ctas']
            ignore_xpath = " or ".join([f"contains(@class, '{cls}')" for cls in ignore_classes])

            article_elements = article.find_elements(
                By.XPATH,
                f".//h1[not(ancestor::*[{ignore_xpath}])] | "
                f".//h2[not(ancestor::*[{ignore_xpath}])] | "
                f".//h3[not(ancestor::*[{ignore_xpath}])] | "
                f".//p[not(ancestor::*[{ignore_xpath}])] | "
                f".//li[not(ancestor::*[{ignore_xpath}])]"
            )

        skip_phrases = []
        if source == "Medium":
            skip_phrases = ["subscribe", "follow", f"{author_blog.lower()}", f"{publisher_blog.lower()}"]
        elif source == "DeepMind":
            skip_phrases = ["research", "impact", "responsibility & safety"]

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
                elif tag_name == "p" and text.lower() not in skip_phrases and not text.isdigit():
                    full_text += f"\n{text}\n"

    except Exception as e:
        full_text = f"Error: {e}"

    finally:
        driver.quit()  # Close the browser

    return full_text.strip()
#=======================================================================================================================
def extract_paper_text(pdf_url):
    """Download PDF and extract text"""
    try:
        # Creation temporary directory for downloaded paper if not exist
        os.makedirs(os.path.join(BASE_DIR, "tmp"), exist_ok=True)

        response = requests.get(pdf_url)

        # Save PDF
        with open(TMP_PDF_PATH, "wb") as f:
            f.write(response.content)

        # Open PDF and extract text
        doc = fitz.open(TMP_PDF_PATH)
        text = "\n".join([page.get_text() for page in doc])

        return text
    except Exception as e:
        print(f"Error: {e}")
        raise
#=======================================================================================================================