# Quick Reference Guide

## 🚀 Getting Started (30 seconds)

```bash
# Clone and setup
git clone <your-repo-url>
cd spam_classifier
pip install -r requirements.txt

# Run full pipeline
make all

# Test the web interface
make run-ui
# Open http://localhost:5001
```

## 📋 Common Commands

### Essential Commands
```bash
make install    # Install dependencies
make prepare    # Prepare dataset
make train      # Train model
make test       # Run tests
make run-ui     # Start web interface
```

### Development Commands
```bash
make test-coverage  # Tests with coverage
make lint           # Check code quality
make format         # Format code
make clean          # Remove generated files
make status         # Check project status
```

### Docker Commands
```bash
make docker-build   # Build image
make docker-run     # Run container
make docker-stop    # Stop container
docker-compose up -d  # Start with compose
```

## 💻 Usage Examples

### Command Line Prediction
```bash
# Direct argument
python src/predict.py "Win free money now!"

# From stdin
echo "Meeting at 3pm" | python src/predict.py

# Interactive mode
python src/predict.py
```

### Python API
```python
from src.predict import predict

# Simple prediction
result = predict("Your message here")
print(result)  # 'spam' or 'ham'

# With confidence
from src.predict import load_model, clean_text
model, vectorizer = load_model()
text = clean_text("Your message")
proba = model.predict_proba(vectorizer.transform([text]))[0]
```

### Web API
```bash
# POST request
curl -X POST http://localhost:5001/classify \
  -H "Content-Type: application/json" \
  -d '{"message": "Your message here"}'

# Response
{"message": "...", "result": "spam", "is_spam": true}
```

## 📊 Project Structure Quick Guide

```
spam_classifier/
├── src/                # Source code
│   ├── prepare.py     # Data preprocessing
│   ├── train.py       # Model training
│   └── predict.py     # Inference
├── ui/                 # Web interface
│   └── app.py         # Flask app
├── tests/             # Test suite
├── docs/              # Documentation
├── data/              # Data files
└── Makefile           # Automation
```

## 🔧 Troubleshooting

### Model Not Found
```bash
# Solution: Train the model
make train
```

### Tests Failing
```bash
# Solution: Ensure model exists
make prepare train test
```

### Port Already in Use
```bash
# Solution: Use different port or kill process
lsof -i :5001
kill -9 <PID>
```

### Dependencies Issue
```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## 📈 Performance Benchmarks

| Metric | Value |
|--------|-------|
| Accuracy | 97.4% |
| Training Time | ~2 seconds |
| Inference Time | <1ms per message |
| Model Size | 1.5 MB |
| Memory Usage | 10 MB |

## 🎯 Key Features Checklist

- ✅ High accuracy (97-98%)
- ✅ Fast inference (<1ms)
- ✅ CLI interface
- ✅ Web interface
- ✅ Complete tests
- ✅ Full documentation
- ✅ Docker support
- ✅ CI/CD ready
- ✅ MIT licensed

## 📚 Documentation Quick Links

- [Overview](docs/overview.md) - Architecture and design
- [Data](docs/data.md) - Dataset information
- [Model](docs/model.md) - Model details
- [Inference](docs/inference.md) - API documentation
- [UI](docs/ui.md) - Web interface
- [Docker](docs/docker.md) - Docker deployment

## 🤝 Contributing Quick Start

```bash
# Fork and clone
git clone <your-fork>
cd spam_classifier

# Setup dev environment
make dev-setup

# Make changes
# ... edit files ...

# Test changes
make test lint

# Commit and push
git add .
git commit -m "Your changes"
git push origin your-branch

# Create pull request
```

## 🔐 Security Notes

- All user input is validated
- No data is logged by default
- Model files should be protected
- Use HTTPS in production
- Implement rate limiting for API

## 📦 Deployment Quick Guide

### Local
```bash
make run-ui
```

### Docker
```bash
docker-compose up -d
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5001 ui.app:app
```

## 🎨 Customization Points

1. **Model**: Change algorithm in `src/train.py`
2. **Features**: Adjust TF-IDF parameters
3. **UI**: Edit `ui/templates/index.html`
4. **API**: Add endpoints in `ui/app.py`
5. **Tests**: Add cases in `tests/`

## 📞 Getting Help

- Check [README.md](README.md) for detailed info
- Read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
- Review [documentation](docs/) for specifics
- Open an issue for bugs
- Start a discussion for questions

---

**Quick Tip**: Run `make help` to see all available commands!
