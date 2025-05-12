# Automatically drafting an engaging blog post based on an academic publication

## Assignment

Generative AI agents are expected to gradually automate routine computer tasks. One such task is producing engaging content oriented to the general public from technical scientific publications.

The student will:
- Review existing recommendations for writing engaging blog posts based on scientific papers
- Review existing works on predicting virality/engagement of a social network post
- Review the available Large Language Models suitable for creating LLM agents
- Create a dataset of papers, corresponding blog posts and the estimates of their success/engagement
- Create a prediction model for predicting the engagement of a blog post based on an LLM
- Design and implement a system that will use LLMs to automatically turn a given scientific paper into a blog post that follows the recommendations and optimizes the engagement
- Evaluate and discuss the strengths and weaknesses of the implemented system

---

## Running the Blog Generation Pipeline

To generate a blog post from a scientific paper, follow these steps:

### 1. Navigate to the project directory

```bash
cd llm_blog_generator
```

### 2. Install required dependencies

```bash
pip install -r requirements.txt
```

### 3. Make the script executable

```bash
chmod +x generate_blog.sh
```

### 4. Add your Google API key

Create a `.env` file in the project root (if it does not already exist) and add your key:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 5. Run the blog generation script

```bash
./generate_blog.sh
```

---

## Optional: Run the Data Preprocessing Notebook

If you'd like to run the Jupyter notebook used for data preprocessing:

### Set the correct ChromeDriver path

In `src/config.py`, update the following line (make sure the appropriate ChromeDriver is installed and the path is valid):

```python
CHROMEDRIVER_PATH = BASE_DIR / "path/to/your/chromedriver"
```

### Download the raw dataset with NIPS papers

You need to download the dataset from Kaggle. You can get it by visiting the following link (last access date: 12-05-2025):  
[Download NIPS Papers Dataset (1987-2019)](https://www.kaggle.com/datasets/rowhitswami/nips-papers-1987-2019-update--d/data?select=papers.csv)  
The reason for downloading the dataset is that the size of the possible attachment for the project did not allow to include the entire dataset.
After downloading, make sure to place the `papers.csv` file in the appropriate directory (`/llm_blog_generator/data/`) as specified in the notebook.