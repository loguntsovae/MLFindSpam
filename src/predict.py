"""
Prediction script for SMS Spam Classifier.
Loads trained model and classifies text from stdin or command line.
"""

import pickle
import sys


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
    
    # Transform text (no cleaning - features are important!)
    text_features = vectorizer.transform([text])
    
    # Predict
    prediction = model.predict(text_features)[0]
    
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
