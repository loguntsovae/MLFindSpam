# Web Interface Documentation

## Overview

The SMS Spam Classifier includes a user-friendly web interface built with Flask. It provides an interactive way to classify messages without using the command line.

![Web UI Screenshot](assets/ui-screenshot.png)

## Features

- 🎨 **Modern Design**: Clean, responsive interface
- ⚡ **Real-time Classification**: Instant results via AJAX
- 📝 **Example Messages**: Pre-filled examples for testing
- 🎯 **Visual Feedback**: Color-coded results (red for spam, green for ham)
- 📱 **Mobile Friendly**: Works on all device sizes
- 🔒 **Client-side Validation**: Input validation before submission

## Quick Start

### Starting the Server

```bash
# Using Make
make run-ui

# Or directly
python ui/app.py
```

The server will start on `http://localhost:5001`

### Accessing the Interface

Open your web browser and navigate to:
```
http://localhost:5001
```

## Architecture

### Backend: Flask Application

**File**: `ui/app.py`

```
┌─────────────────────┐
│   Browser Client    │
│  (JavaScript/HTML)  │
└──────────┬──────────┘
           │ HTTP POST /classify
           ▼
┌─────────────────────┐
│   Flask Server      │
│   Port 5001         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Prediction Module  │
│  (src/predict.py)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Trained Model     │
│   (model.pkl)       │
└─────────────────────┘
```

### Frontend: HTML + JavaScript

**File**: `ui/templates/index.html`

- **HTML**: Structure and form
- **CSS**: Styling with gradient backgrounds
- **JavaScript**: AJAX requests and dynamic updates

## API Endpoints

### `GET /`

Renders the main web interface.

**Response**: HTML page

**Example**:
```bash
curl http://localhost:5001/
```

### `POST /classify`

Classifies a message and returns the result.

**Request Body** (JSON):
```json
{
  "message": "Win free money now!"
}
```

**Request Body** (Form Data):
```
message=Win+free+money+now!
```

**Response** (Success):
```json
{
  "message": "Win free money now!",
  "result": "spam",
  "is_spam": true
}
```

**Response** (Error):
```json
{
  "error": "No message provided"
}
```

**Status Codes**:
- `200 OK`: Classification successful
- `400 Bad Request`: Invalid input
- `500 Internal Server Error`: Server error

**Example**:
```bash
# Using curl with JSON
curl -X POST http://localhost:5001/classify \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello friend"}'

# Using curl with form data
curl -X POST http://localhost:5001/classify \
  -d "message=Hello friend"
```

## User Interface

### Main Components

1. **Header**
   - Title: "SMS Spam Classifier"
   - Subtitle: "Detect whether a message is spam or legitimate"

2. **Input Form**
   - Large text area for message input
   - Placeholder text with example
   - Submit button: "Classify Message"

3. **Results Display**
   - Shows classification result
   - Color-coded: Red (spam), Green (ham)
   - Includes explanation text

4. **Example Messages**
   - 4 clickable examples (2 spam, 2 ham)
   - Auto-fills input when clicked
   - Helps users test the system

### User Flow

```
1. User opens website
        ↓
2. User enters/selects message
        ↓
3. User clicks "Classify Message"
        ↓
4. JavaScript sends POST to /classify
        ↓
5. Server processes and responds
        ↓
6. Result displayed with color coding
```

## Customization

### Changing Port

Edit `ui/app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Change port here
```

### Modifying Styles

Edit CSS in `ui/templates/index.html`:
```css
/* Change color scheme */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Your custom gradient here */
}

/* Change result colors */
.result.spam {
    background: #fee;  /* Light red */
    border: 2px solid #fcc;
}

.result.ham {
    background: #efe;  /* Light green */
    border: 2px solid #cfc;
}
```

### Adding Features

Add new endpoint to `ui/app.py`:
```python
@app.route('/batch', methods=['POST'])
def classify_batch():
    data = request.get_json()
    messages = data.get('messages', [])
    
    results = [predict(msg) for msg in messages]
    
    return jsonify({
        'results': results,
        'count': len(results)
    })
```

## Deployment

### Local Development

```bash
# Development mode (auto-reload)
export FLASK_ENV=development
python ui/app.py
```

### Production with Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5001 ui.app:app
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt gunicorn

COPY . .
RUN python src/train.py

EXPOSE 5001
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "ui.app:app"]
```

Build and run:
```bash
docker build -t spam-classifier .
docker run -p 5001:5001 spam-classifier
```

### Cloud Deployment

#### Heroku

Create `Procfile`:
```
web: gunicorn ui.app:app
```

Deploy:
```bash
heroku create spam-classifier
git push heroku main
```

#### AWS Elastic Beanstalk

Create `.ebextensions/python.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: ui.app:app
```

Deploy:
```bash
eb init -p python-3.9 spam-classifier
eb create spam-classifier-env
```

#### Google Cloud Run

```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/spam-classifier

# Deploy
gcloud run deploy --image gcr.io/PROJECT_ID/spam-classifier --platform managed
```

## Security

### Input Validation

```python
@app.route('/classify', methods=['POST'])
def classify():
    message = request.get_json().get('message', '')
    
    # Validate input
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    if len(message) > 1000:
        return jsonify({'error': 'Message too long'}), 400
    
    # Sanitize input (remove control characters)
    message = ''.join(char for char in message if char.isprintable())
    
    result = predict(message)
    return jsonify({'result': result})
```

### CORS (Cross-Origin Resource Sharing)

For API access from other domains:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/classify": {"origins": "https://yourdomain.com"}})
```

### Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)

@app.route('/classify', methods=['POST'])
@limiter.limit("10 per minute")
def classify():
    # Classification logic
    pass
```

### HTTPS

Use a reverse proxy like Nginx:
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Performance Optimization

### Caching Model

Load model once at startup:
```python
from src.predict import load_model

# Global variable
model, vectorizer = load_model()

@app.route('/classify', methods=['POST'])
def classify():
    message = request.get_json().get('message', '')
    
    # Use cached model
    cleaned = clean_text(message)
    features = vectorizer.transform([cleaned])
    result = model.predict(features)[0]
    
    return jsonify({'result': result})
```

### Async Processing

For heavy loads, use Celery:
```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def classify_async(message):
    return predict(message)

@app.route('/classify', methods=['POST'])
def classify():
    message = request.get_json().get('message', '')
    task = classify_async.delay(message)
    
    return jsonify({'task_id': task.id})
```

### Static File Caching

```python
@app.route('/static/<path:filename>')
def static_files(filename):
    response = send_from_directory('static', filename)
    response.cache_control.max_age = 3600  # 1 hour
    return response
```

## Monitoring

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    message = request.get_json().get('message', '')
    logger.info(f"Received classification request (length: {len(message)})")
    
    result = predict(message)
    logger.info(f"Classification result: {result}")
    
    return jsonify({'result': result})
```

### Metrics

```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)

# Automatic metrics:
# - Request count
# - Request duration
# - Request size

# Custom metrics
classification_counter = metrics.counter(
    'classifications_total',
    'Total number of classifications',
    labels={'result': lambda: 'spam' if result == 'spam' else 'ham'}
)
```

## Testing

### Unit Tests

```python
# tests/test_ui.py
import pytest
from ui.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'SMS Spam Classifier' in response.data

def test_classify_spam(client):
    response = client.post('/classify', json={
        'message': 'WIN FREE MONEY NOW'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 'spam'

def test_classify_ham(client):
    response = client.post('/classify', json={
        'message': 'Meeting at 3pm'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 'ham'

def test_empty_message(client):
    response = client.post('/classify', json={'message': ''})
    assert response.status_code == 400
```

### Integration Tests

```bash
# Start server
python ui/app.py &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Test endpoint
curl -X POST http://localhost:5001/classify \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}' \
  | grep -q "result"

# Check exit code
if [ $? -eq 0 ]; then
    echo "✓ Integration test passed"
else
    echo "✗ Integration test failed"
fi

# Stop server
kill $SERVER_PID
```

## Troubleshooting

### Server Won't Start

**Problem**: `Address already in use`
```
OSError: [Errno 48] Address already in use
```

**Solution**:
```bash
# Find process using port 5001
lsof -i :5001

# Kill process
kill -9 <PID>

# Or use different port
python ui/app.py --port 5002
```

### Model Not Found

**Problem**: `FileNotFoundError: model.pkl not found`

**Solution**:
```bash
# Train model first
python src/train.py

# Verify model exists
ls -lh model.pkl
```

### Template Not Found

**Problem**: `TemplateNotFound: index.html`

**Solution**:
```bash
# Check templates directory
ls ui/templates/

# Ensure Flask knows template location
# In app.py:
app = Flask(__name__, template_folder='templates')
```

## Best Practices

1. **Error Handling**: Always validate input and handle exceptions
2. **Security**: Implement rate limiting and input sanitization
3. **Performance**: Cache model, use connection pooling
4. **Monitoring**: Log requests and track metrics
5. **Testing**: Write tests for all endpoints
6. **Documentation**: Keep API docs up to date
7. **Deployment**: Use production WSGI server (Gunicorn, uWSGI)

## Future Enhancements

- Add user authentication
- Implement batch classification
- Add classification history
- Export results to CSV
- Add confidence scores display
- Implement dark mode
- Add multilingual support
- Create mobile app
- Add REST API documentation (Swagger/OpenAPI)
- Implement WebSocket for real-time updates

## References

- Flask Documentation: https://flask.palletsprojects.com/
- Bootstrap CSS: https://getbootstrap.com/
- AJAX Tutorial: https://developer.mozilla.org/en-US/docs/Web/Guide/AJAX
- Deployment Guide: https://flask.palletsprojects.com/en/2.0.x/deploying/
