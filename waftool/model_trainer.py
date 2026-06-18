import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import joblib
import os

def get_data():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Use extended dataset
    csv_path = os.path.join(script_dir, 'sqli-extended.csv')
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Please create it first.")
        # Fallback or exit
        return pd.DataFrame(columns=['payload', 'is_malicious'])
    
    print(f"Loading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Map columns to expected names if necessary
    # The file has 'Sentence' and 'Label'
    if 'Sentence' in df.columns and 'Label' in df.columns:
        df = df.rename(columns={'Sentence': 'payload', 'Label': 'is_malicious'})
    
    # Ensure columns exist
    if 'payload' not in df.columns or 'is_malicious' not in df.columns:
        raise ValueError("CSV must contain 'payload' and 'is_malicious' columns (or 'Sentence' and 'Label').")
        
    # Drop NaNs just in case
    df = df.dropna()
    # Ensure label is int
    df['is_malicious'] = df['is_malicious'].astype(int)
    
    return df

def train_model():
    print("Generating dataset...")
    df = get_data()
    
    X = df['payload']
    y = df['is_malicious']
    
    # Simple split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training model...")
    # Create a pipeline that vectorizes the text and then applies Logistic Regression
    # analyzer='char' is used to capture character-level patterns (like quotes, dashes) often found in SQLi
    # ngram_range=(1, 4) captures sequences of characters
    pipeline = make_pipeline(
        CountVectorizer(analyzer='char', ngram_range=(1, 4)),
        LogisticRegression()
    )
    
    pipeline.fit(X_train, y_train)
    
    print(f"Training Accuracy: {pipeline.score(X_train, y_train)}")
    print(f"Test Accuracy: {pipeline.score(X_test, y_test)}")
    
    # Save the model in the waftool directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'firewall_model.pkl')
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
