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
cd llm_blog_generator/
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
CHROMEDRIVER_PATH = "absolute/path/to/your/chromedriver"
```

### Download the raw dataset with NIPS papers

#### 1. Navigate to the script directory

```bash
cd llm_blog_generator/data/
```

#### 2. Make the script executable

```bash
chmod +x download_dataset.sh
```

#### 3. Run the script

```bash
./download_dataset.sh
```