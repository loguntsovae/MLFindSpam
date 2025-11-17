"""
Flask web interface for SMS Spam Classifier.
Provides a simple form to classify messages.
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path to import predict module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.predict import predict

app = Flask(__name__)


@app.route('/')
def index():
    """Render the main page with input form."""
    return render_template('index.html')


@app.route('/classify', methods=['POST'])
def classify():
    """
    Handle classification request.
    Accepts JSON with 'message' field or form data.
    """
    # Get message from JSON or form data
    if request.is_json:
        data = request.get_json()
        message = data.get('message', '')
    else:
        message = request.form.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Predict
        result = predict(message)
        
        # Determine if spam or ham
        is_spam = (result == 'spam')
        
        return jsonify({
            'message': message,
            'result': result,
            'is_spam': is_spam
        })
    
    except FileNotFoundError:
        return jsonify({
            'error': 'Model not found. Please train the model first.'
        }), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
