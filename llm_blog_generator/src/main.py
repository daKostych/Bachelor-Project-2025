import sys
import os
import warnings
from pathlib import Path

if str(Path().resolve().parent) not in sys.path:
    sys.path.append(str(Path().resolve().parent))

warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
google_api_key = None
try:
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if google_api_key:
        print("Successfully loaded Google API key from environment variables.")
    else:
        print("Google API key is not set in environment variables.")
        sys.exit("Google API key is required. Set it in environment variables.")
except Exception as e:
    print(f"Error loading environment variables: {e}")
    raise

# Configure Google API
try:
    genai.configure(api_key=google_api_key)
    print("Google API successfully configured with the API key.")
except Exception as e:
    print(f"Error configuring Google API: {e}")
    raise

from src.blog_generator import BlogGenerator

def number_from_interval(query, number_interval):
    while True:
        try:
            number = int(input(query).strip())
            if number_interval[0] <= number <= number_interval[1]:
                return number
            else:
                print(f"Please enter an integer number between "
                      f"{number_interval[0]} and {number_interval[1]} inclusive.")
                continue
        except ValueError:
            print("Invalid input. Try again.")

def yes_or_no(question):
    while True:
        answer_yes_no = input(question).strip().lower()
        if answer_yes_no == "yes":
            return True
        elif answer_yes_no == "no":
            return False
        else:
            print("Invalid answer. Please enter yes or no.")

def answer_from_choices(question, choices):
    while True:
        ans = input(f"{question} ({'/'.join(choices)}): ")
        if ans in choices:
            return ans
        else:
            print(f"Invalid answer. Please choose from {choices}.")

def read_paper(query):
    while True:
        path = input(query).strip()
        if not os.path.isfile(path):
            print("File does not exist. Please enter a valid path.")
            continue
        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as error:
            print(f"Failed to read file.\n{error}")
            raise

if __name__ == "__main__":
    # Collecting parameters for blog generator
    interval = (1, 5)
    max_attempts = number_from_interval(f"Maximum number of blog generation attempts "
                                        f"(from interval [{interval[0]}, {interval[1]}]): ",
                                        interval)
    max_attempts_call = number_from_interval(f"Maximum number of attempts to get a valid response from the model "
                                             f"(from interval [{interval[0]}, {interval[1]}]): ",
                                             interval)
    use_reflexion = yes_or_no("Do you want to enable self-reflection mechanism? (yes/no): ")
    use_memory = yes_or_no("Do you want to use the long-term memory module? (yes/no): ")
    print()

    generator = BlogGenerator(max_attempts=max_attempts,
                              max_attempts_call=max_attempts_call,
                              use_memory=use_memory,
                              use_reflexion=use_reflexion)
    print()

    paper_info = answer_from_choices("In what format is your scientific paper available?",
                                     ["arxiv pdf URL", "full text"])
    blog = None
    if paper_info == "arxiv pdf URL":
        paper_url = input("Enter the paper arxiv pdf URL: ").strip()
        blog = generator.generate_blog(paper_url=paper_url)
    elif paper_info == "full text":
        paper_text = read_paper("Enter the absolute path to the file containing the paper text: ")
        blog = generator.generate_blog(paper_text=paper_text)

    if blog:
        print("Check out the blog!")