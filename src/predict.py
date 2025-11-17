"""
Prediction script for SMS Spam Classifier.
Loads trained model and classifies text from stdin or command line.
"""

import pickle
import sys
import re


def clean_text(text):
    """Clean and normalize text data (same as in prepare.py)."""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def load_model(model_path='model.pkl'):
    """Load the trained model and vectorizer."""
    with open(model_path, 'rb') as f:
        data = pickle.load(f)
    return data['model'], data['vectorizer']


def predict(text, model_path='model.pkl'):
    """
    Predict whether a text message is spam or ham.
    
    Args:
        text: Message text to classify
        model_path: Path to trained model
        
    Returns:
        'spam' or 'ham'
    """
    # Load model
    model, vectorizer = load_model(model_path)
    
    # Clean text
    cleaned_text = clean_text(text)
    
    # Transform text
    text_tfidf = vectorizer.transform([cleaned_text])
    
    # Predict
    prediction = model.predict(text_tfidf)[0]
    
    return prediction


def main():
    """Main function for CLI usage."""
    if len(sys.argv) > 1:
        # Text provided as command line argument
        text = ' '.join(sys.argv[1:])
    else:
        # Read from stdin
        print("Enter message to classify (or Ctrl+D to exit):")
        text = sys.stdin.read().strip()
    
    if not text:
        print("Error: No text provided", file=sys.stderr)
        sys.exit(1)
    
    try:
        result = predict(text)
        print(result)
    except FileNotFoundError:
        print("Error: Model file 'model.pkl' not found. Please train the model first.", 
              file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
