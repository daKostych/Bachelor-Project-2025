import pandas as pd
from sklearn import model_selection
from src import random_seed
from src.config import DATASET_PATH
#=======================================================================================================================
def load_dataset(dataset_path=DATASET_PATH):
    """Import and preprocess data"""
    data = pd.read_csv(dataset_path) # Import

    # Correcting URL of the paper if needed
    data["url_paper"] = data["url_paper"].str.replace("abs", "pdf", regex=False)

    # Calculate engagement score
    data["engagement_score"] = (data["claps"] + 3 * data["comments"]) / data["author_followers"]
    min_val = data["engagement_score"].min()
    max_val = data["engagement_score"].nlargest(3).iloc[-1] # Ignore 2 outliers
    data["normalized_engagement_score"] = 100 * (data["engagement_score"] - min_val) / (max_val - min_val) # Experimental MinMax normalization
    data["normalized_engagement_score"] = round(data["normalized_engagement_score"].clip(1, 100))

    return data
#=======================================================================================================================
def validation_test_split(data, test_size=0.4):
    """Split dataset into validation and test set"""
    Xval, Xtest, yval, ytest = model_selection.train_test_split(
        data.drop(columns=['normalized_engagement_score']), data["normalized_engagement_score"],
        test_size=0.4, random_state=random_seed)

    return Xval, Xtest, yval, ytest
#=======================================================================================================================