"""
Model training script for SMS Spam Classifier.
Trains a LogisticRegression model with TF-IDF vectorization.
"""

import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os


def train_model(train_path='data/train.csv', test_path='data/test.csv', 
                model_path='model.pkl'):
    """
    Train a spam classifier using LogisticRegression and TF-IDF.
    
    Args:
        train_path: Path to training data
        test_path: Path to test data
        model_path: Path to save trained model
    """
    print("Loading training data...")
    train_df = pd.read_csv(train_path)
    
    print("Loading test data...")
    test_df = pd.read_csv(test_path)
    
    # Prepare data
    X_train = train_df['message']
    y_train = train_df['label']
    X_test = test_df['message']
    y_test = test_df['label']
    
    print("\nTraining TF-IDF Vectorizer...")
    # Initialize TF-IDF Vectorizer with multilingual support
    vectorizer = TfidfVectorizer(
        max_features=5000,  # Increased for multilingual
        min_df=1,  # More flexible for smaller Russian dataset
        max_df=0.85,
        ngram_range=(1, 3),  # Tri-grams for better pattern detection
        analyzer='char_wb',  # Character n-grams work better for Russian
        lowercase=True,
        # Removed stop_words to support both languages
    )
    
    # Fit and transform training data
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"Feature matrix shape: {X_train_tfidf.shape}")
    
    print("\nTraining Logistic Regression model...")
    # Train Logistic Regression with optimized parameters
    model = LogisticRegression(
        max_iter=2000,  # Increased iterations
        random_state=42,
        C=0.5,  # Regularization for better generalization
        solver='saga',  # Better for large datasets and multilingual
        class_weight='balanced',  # Handle class imbalance
        penalty='l2'
    )
    
    model.fit(X_train_tfidf, y_train)
    
    # Evaluate on training set
    y_train_pred = model.predict(X_train_tfidf)
    train_accuracy = accuracy_score(y_train, y_train_pred)
    
    # Evaluate on test set
    y_test_pred = model.predict(X_test_tfidf)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    
    print("\n" + "="*50)
    print("MODEL PERFORMANCE")
    print("="*50)
    print(f"\nTrain Accuracy: {train_accuracy:.4f}")
    print(f"Test Accuracy:  {test_accuracy:.4f}")
    
    print("\n" + "-"*50)
    print("Classification Report (Test Set):")
    print("-"*50)
    print(classification_report(y_test, y_test_pred))
    
    print("-"*50)
    print("Confusion Matrix (Test Set):")
    print("-"*50)
    print(confusion_matrix(y_test, y_test_pred))
    print()
    
    # Save the model and vectorizer
    print(f"\nSaving model to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump({
            'model': model,
            'vectorizer': vectorizer
        }, f)
    
    print("\nTraining completed successfully!")
    
    return {
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'model': model,
        'vectorizer': vectorizer
    }


if __name__ == '__main__':
    train_model()
