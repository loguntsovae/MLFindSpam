# Inference Documentation

## Overview

The inference module (`src/predict.py`) provides functionality to classify SMS messages using the trained model. It supports both command-line and programmatic usage.

## Quick Start

### Command Line

```bash
# From command line argument
python src/predict.py "Win a free iPhone now!"
# Output: spam

# From stdin
echo "Hey, see you tomorrow" | python src/predict.py
# Output: ham

# Interactive mode
python src/predict.py
# Enter message to classify (or Ctrl+D to exit):
# > Your message here
# Output: ham or spam
```

### Python API

```python
from src.predict import predict

# Simple prediction
result = predict("Congratulations! You won $1000")
print(result)  # Output: spam

# Use with custom model path
result = predict("Hello friend", model_path="models/model_v2.pkl")
```

## API Reference

### `predict(text, model_path='model.pkl')`

Classify a text message as spam or ham.

**Parameters**:
- `text` (str): The message to classify
- `model_path` (str, optional): Path to the trained model file. Default: 'model.pkl'

**Returns**:
- `str`: Either 'spam' or 'ham'

**Raises**:
- `FileNotFoundError`: If model file doesn't exist
- `ValueError`: If text is empty after cleaning

**Example**:
```python
>>> from src.predict import predict
>>> predict("FREE prize claim now!")
'spam'
>>> predict("Meeting at 3pm in room 101")
'ham'
```

### `clean_text(text)`

Clean and normalize text using the same preprocessing as training.

**Parameters**:
- `text` (str): Raw text to clean

**Returns**:
- `str`: Cleaned text

**Transformations**:
1. Convert to lowercase
2. Remove URLs
3. Normalize whitespace
4. Strip leading/trailing spaces

**Example**:
```python
>>> from src.predict import clean_text
>>> clean_text("Check THIS http://spam.com NOW!!!")
'check  now!!!'
```

### `load_model(model_path='model.pkl')`

Load the trained model and vectorizer from disk.

**Parameters**:
- `model_path` (str, optional): Path to model file

**Returns**:
- `tuple`: (model, vectorizer)

**Example**:
```python
>>> from src.predict import load_model
>>> model, vectorizer = load_model()
>>> type(model)
<class 'sklearn.linear_model.LogisticRegression'>
```

## Usage Patterns

### Batch Processing

Process multiple messages at once:

```python
from src.predict import predict

messages = [
    "Win free money now!",
    "Meeting tomorrow at 2pm",
    "Claim your prize today",
    "Can you pick up groceries?"
]

results = [predict(msg) for msg in messages]
print(results)
# ['spam', 'ham', 'spam', 'ham']
```

### With Confidence Scores

Get prediction probabilities:

```python
from src.predict import load_model, clean_text

model, vectorizer = load_model()
text = "Free entry to win prizes"
cleaned = clean_text(text)
features = vectorizer.transform([cleaned])

# Get probabilities [ham_prob, spam_prob]
probabilities = model.predict_proba(features)[0]
prediction = model.predict(features)[0]

print(f"Prediction: {prediction}")
print(f"Confidence: {max(probabilities):.2%}")
# Prediction: spam
# Confidence: 95.3%
```

### Error Handling

```python
from src.predict import predict

try:
    result = predict("Your message")
    print(f"Classification: {result}")
except FileNotFoundError:
    print("Model not found. Please run training first.")
    print("Command: python src/train.py")
except Exception as e:
    print(f"Error during prediction: {e}")
```

## Integration Examples

### Flask Web Service

```python
from flask import Flask, request, jsonify
from src.predict import predict

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        result = predict(message)
        return jsonify({
            'message': message,
            'classification': result,
            'is_spam': result == 'spam'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.predict import predict

app = FastAPI()

class Message(BaseModel):
    text: str

@app.post("/classify")
async def classify_message(message: Message):
    try:
        result = predict(message.text)
        return {
            "classification": result,
            "is_spam": result == "spam"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Command Line Tool

```python
import sys
import argparse
from src.predict import predict

def main():
    parser = argparse.ArgumentParser(
        description='Classify SMS messages as spam or ham'
    )
    parser.add_argument(
        'message',
        nargs='*',
        help='Message to classify (or use stdin)'
    )
    parser.add_argument(
        '--model',
        default='model.pkl',
        help='Path to model file'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    
    args = parser.parse_args()
    
    # Get message from args or stdin
    if args.message:
        text = ' '.join(args.message)
    else:
        text = sys.stdin.read().strip()
    
    # Predict
    result = predict(text, model_path=args.model)
    
    if args.verbose:
        print(f"Input: {text}")
        print(f"Classification: {result}")
    else:
        print(result)

if __name__ == '__main__':
    main()
```

## Performance

### Latency

| Operation | Time |
|-----------|------|
| Model loading | ~50ms (one-time) |
| Text cleaning | ~0.1ms |
| Vectorization | ~0.3ms |
| Prediction | ~0.1ms |
| **Total per message** | **~0.5ms** |

### Throughput

- **Single thread**: ~2,000 messages/second
- **With batching**: ~5,000 messages/second
- **Memory usage**: ~10MB (model loaded)

### Optimization Tips

1. **Load model once**: Cache the model in memory
2. **Batch predictions**: Process multiple messages together
3. **Use sparse matrices**: TF-IDF outputs are sparse
4. **Precompile regex**: Cache regex patterns for cleaning

## Error Handling

### Common Errors

1. **Model Not Found**
   ```
   FileNotFoundError: Model file 'model.pkl' not found
   Solution: Run `python src/train.py` to train the model
   ```

2. **Empty Input**
   ```
   Error: No text provided
   Solution: Provide a non-empty message
   ```

3. **Corrupted Model**
   ```
   pickle.UnpicklingError: invalid load key
   Solution: Retrain the model or restore from backup
   ```

4. **Version Mismatch**
   ```
   ModuleNotFoundError: No module named 'sklearn'
   Solution: Install dependencies with `pip install -r requirements.txt`
   ```

## Testing

### Unit Tests

```python
# tests/test_predict.py
from src.predict import predict, clean_text

def test_spam_detection():
    result = predict("WIN FREE MONEY NOW!!!")
    assert result == 'spam'

def test_ham_detection():
    result = predict("Meeting at 3pm")
    assert result == 'ham'

def test_text_cleaning():
    cleaned = clean_text("  Hello   World  ")
    assert cleaned == "hello world"
```

Run tests:
```bash
pytest tests/test_predict.py -v
```

### Integration Tests

```bash
# Test CLI interface
echo "Free prize!" | python src/predict.py
# Should output: spam

python src/predict.py "See you tomorrow"
# Should output: ham
```

## Security Considerations

1. **Input Validation**: Always validate and sanitize input
2. **Length Limits**: Set maximum message length (e.g., 1000 chars)
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **No Data Logging**: Don't log user messages by default
5. **Model Security**: Protect model files from unauthorized access

## Deployment

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python src/train.py

CMD ["python", "ui/app.py"]
```

### AWS Lambda

```python
import json
from src.predict import predict

def lambda_handler(event, context):
    body = json.loads(event['body'])
    message = body.get('message', '')
    
    result = predict(message)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'classification': result,
            'is_spam': result == 'spam'
        })
    }
```

## Monitoring

### Metrics to Track

1. **Prediction Latency**: p50, p95, p99 response times
2. **Throughput**: Requests per second
3. **Error Rate**: Failed predictions / total predictions
4. **Spam Rate**: Percentage of messages classified as spam
5. **Model Confidence**: Distribution of prediction probabilities

### Logging

```python
import logging
from src.predict import predict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def predict_with_logging(text):
    logger.info(f"Classifying message (length: {len(text)})")
    result = predict(text)
    logger.info(f"Classification: {result}")
    return result
```

## Troubleshooting

### Model Not Loading

**Problem**: `FileNotFoundError: model.pkl not found`

**Solution**:
```bash
# Train the model first
python src/train.py

# Verify model exists
ls -lh model.pkl
```

### Poor Predictions

**Problem**: Model giving incorrect predictions

**Solutions**:
1. Check if model is trained: `ls -lh model.pkl`
2. Verify data quality: `head data/train.csv`
3. Retrain model: `make train`
4. Check scikit-learn version: `pip show scikit-learn`

### Slow Performance

**Problem**: Predictions taking too long

**Solutions**:
1. Cache model in memory (don't reload for each prediction)
2. Use batch prediction for multiple messages
3. Profile code: `python -m cProfile src/predict.py "test"`

## Best Practices

1. **Load model once**: Cache at application startup
2. **Validate input**: Check for empty, too long, or invalid input
3. **Handle errors gracefully**: Return meaningful error messages
4. **Log predictions**: For monitoring and debugging
5. **Monitor performance**: Track latency and accuracy
6. **Version models**: Keep track of model versions in production
7. **A/B test**: Test new models before full deployment

## References

- scikit-learn documentation: https://scikit-learn.org/
- Flask documentation: https://flask.palletsprojects.com/
- Deployment best practices: https://ml-ops.org/
