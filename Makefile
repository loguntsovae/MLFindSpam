.PHONY: all prepare train test run-ui clean help install predict test-coverage lint format docker-build docker-run docker-stop docker-restart docker-up docker-down docker-compose-rebuild russian-merge russian-train russian-test

# Python command
PYTHON = python3

# Default target
all: prepare train test

# Help command
help:
	@echo "SMS Spam Classifier - Makefile Commands"
	@echo "========================================"
	@echo "Development Commands:"
	@echo "  make install       - Install all dependencies"
	@echo "  make prepare       - Download and prepare data (train/test split)"
	@echo "  make train         - Train the spam classifier model"
	@echo "  make test          - Run unit tests with pytest"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo "  make lint          - Run code quality checks"
	@echo "  make format        - Format code with black"
	@echo ""
	@echo "Running Commands:"
	@echo "  make run-ui        - Start Flask web interface"
	@echo "  make predict       - Interactive prediction mode"
	@echo ""
	@echo "🇷🇺 Russian Language Commands:"
	@echo "  make russian-merge - Merge Russian dataset with main dataset"
	@echo "  make russian-train - Full pipeline with Russian data (merge + train)"
	@echo "  make russian-test  - Test model with Russian examples"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"
	@echo "  make docker-stop   - Stop Docker container"
	@echo "  make docker-restart - Rebuild and restart container"
	@echo "  make docker-compose-rebuild - Rebuild with docker-compose"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean         - Remove generated files (model, data splits)"
	@echo "  make clean-all     - Remove all generated files including caches"
	@echo "  make all           - Run full pipeline (prepare + train + test)"
	@echo ""

# Install dependencies
install:
	@echo "==> Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	pip install -r requirements.txt
	@echo "✓ Dependencies installed!"

# Prepare data: download and split into train/test
prepare:
	@echo "==> Preparing data..."
	$(PYTHON) src/prepare.py
	@echo "✓ Data preparation complete!"

# Train the model
train:
	@echo "==> Training model..."
	$(PYTHON) src/train.py
	@echo "✓ Model training complete!"

# Run tests
test:
	@echo "==> Running tests..."
	$(PYTHON) -m pytest tests/test_predict.py -v
	@echo "✓ Tests complete!"

# Run web UI
run-ui:
	@echo "==> Starting web interface..."
	@echo "✓ Open http://localhost:5001 in your browser"
	$(PYTHON) ui/app.py

# Clean generated files
clean:
	@echo "==> Cleaning generated files..."
	rm -f model.pkl
	rm -f data/train.csv data/test.csv
	@echo "✓ Cleanup complete!"

# Clean all including caches
clean-all: clean
	@echo "==> Deep cleaning..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	@echo "✓ Deep cleanup complete!"

# Quick test prediction
predict:
	@echo "Enter message to classify:"
	@$(PYTHON) src/predict.py

# Run with coverage
test-coverage:
	@echo "==> Running tests with coverage..."
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
	@echo "✓ Coverage report complete! Open htmlcov/index.html to view"

# Lint code
lint:
	@echo "==> Running code quality checks..."
	@echo "Checking with flake8..."
	-$(PYTHON) -m flake8 src/ tests/ ui/ --max-line-length=127 --statistics || true
	@echo "Checking with pylint..."
	-$(PYTHON) -m pylint src/ tests/ ui/ --max-line-length=127 || true
	@echo "✓ Linting complete!"

# Format code
format:
	@echo "==> Formatting code with black..."
	$(PYTHON) -m black src/ tests/ ui/ --line-length=127
	@echo "✓ Code formatting complete!"

# Docker build
docker-build:
	@echo "==> Building Docker image..."
	docker build -t spam-classifier:latest .
	@echo "✓ Docker image built!"

# Docker run
docker-run:
	@echo "==> Starting Docker container..."
	docker run -d --name spam_classifier -p 5001:5001 spam-classifier:latest
	@echo "✓ Container started! Access at http://localhost:5001"

# Docker stop
docker-stop:
	@echo "==> Stopping Docker container..."
	docker stop spam_classifier || true
	docker rm spam_classifier || true
	@echo "✓ Container stopped!"

# Docker rebuild and restart
docker-restart: docker-stop docker-build docker-run
	@echo "✓ Container rebuilt and restarted!"

# Docker compose
docker-up:
	@echo "==> Starting services with docker-compose..."
	docker-compose up -d
	@echo "✓ Services started!"

docker-down:
	@echo "==> Stopping services..."
	docker-compose down
	@echo "✓ Services stopped!"

# Docker compose rebuild
docker-compose-rebuild:
	@echo "==> Rebuilding and restarting services..."
	docker-compose down
	docker-compose up --build -d
	@echo "✓ Services rebuilt and restarted!"

# 🇷🇺 Russian language support commands
russian-merge:
	@echo "==> 🇷🇺 Merging Russian dataset with main dataset..."
	$(PYTHON) src/merge_russian_data.py --update-raw
	@echo "✓ Russian data merged! Original backed up as raw_english_only.csv"

russian-train: russian-merge
	@echo "==> 🇷🇺 Training multilingual model..."
	$(PYTHON) src/prepare.py
	$(PYTHON) src/train.py
	@echo "✓ Multilingual model trained!"

russian-test:
	@echo "==> 🇷🇺 Testing model with Russian examples..."
	$(PYTHON) src/test_russian.py
	@echo "✓ Russian test complete!"

# Check project status
status:
	@echo "==> Project Status"
	@echo "=================="
	@echo "Data files:"
	@ls -lh data/*.csv 2>/dev/null || echo "  No data files found"
	@echo ""
	@echo "Model file:"
	@ls -lh model.pkl 2>/dev/null || echo "  No model file found"
	@echo ""
	@echo "Python version:"
	@$(PYTHON) --version
	@echo ""
	@echo "Dependencies:"
	@pip list | grep -E "(pandas|scikit-learn|flask|pytest)" || echo "  Not installed"

# Setup development environment
dev-setup: install
	@echo "==> Setting up development environment..."
	pip install black flake8 pylint pytest-cov
	@echo "✓ Development environment ready!"

# Run full pipeline
pipeline: clean install prepare train test
	@echo "✓ Full pipeline completed successfully!"
