"""
Data preparation script for SMS Spam Classifier.
Reads raw.csv, cleans text, and splits into train/test sets (80/20).
"""

import pandas as pd
import re
from sklearn.model_selection import train_test_split
import os


def clean_text(text):
    """Clean and normalize text data."""
    # Convert to lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def prepare_data(input_path='data/raw.csv', output_dir='data'):
    """
    Load, clean, and split the SMS dataset.
    
    Args:
        input_path: Path to raw CSV file
        output_dir: Directory to save train/test CSVs
    """
    print(f"Loading data from {input_path}...")
    
    # Load the dataset
    # SMS Spam Collection format: v1 (label), v2 (message)
    df = pd.read_csv(input_path, encoding='latin-1')
    
    # Keep only relevant columns
    df = df[['v1', 'v2']]
    df.columns = ['label', 'message']
    
    # Clean the text
    print("Cleaning text data...")
    df['message'] = df['message'].apply(clean_text)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['message'])
    
    # Remove empty messages
    df = df[df['message'].str.len() > 0]
    
    print(f"Total samples: {len(df)}")
    print(f"Spam: {len(df[df['label'] == 'spam'])}")
    print(f"Ham: {len(df[df['label'] == 'ham'])}")
    
    # Split into train and test sets (80/20)
    train_df, test_df = train_test_split(
        df, 
        test_size=0.2, 
        random_state=42, 
        stratify=df['label']
    )
    
    # Save to CSV
    train_path = os.path.join(output_dir, 'train.csv')
    test_path = os.path.join(output_dir, 'test.csv')
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f"\nTrain set: {len(train_df)} samples -> {train_path}")
    print(f"Test set: {len(test_df)} samples -> {test_path}")
    print("\nData preparation completed successfully!")


if __name__ == '__main__':
    prepare_data()
