# SMS Spam Classifier - Project Overview

## Introduction

SMS Spam Classifier is a complete machine learning pipeline designed to detect spam messages in SMS text. This project demonstrates best practices in ML engineering, including data preprocessing, model training, evaluation, deployment, and testing.

## Project Goals

1. **Educational**: Serve as a reference implementation for ML projects
2. **Production-Ready**: Include all components needed for real-world deployment
3. **Well-Documented**: Provide comprehensive documentation for learning
4. **Maintainable**: Follow clean code principles and testing best practices

## Architecture

### High-Level Design

```
┌─────────────┐
│  Raw Data   │
│  (SMS CSV)  │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│  Data Pipeline   │
│  - Text Cleaning │
│  - Train/Test    │
│    Split         │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Training        │
│  - TF-IDF        │
│  - Logistic Reg  │
│  - Evaluation    │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Saved Model     │
│  (model.pkl)     │
└──────┬───────────┘
       │
       ├─────────────┐
       │             │
       ▼             ▼
┌──────────┐  ┌──────────┐
│   CLI    │  │  Web UI  │
│ Interface│  │  (Flask) │
└──────────┘  └──────────┘
```

## Components

### 1. Data Preparation (`src/prepare.py`)

**Purpose**: Load, clean, and prepare data for training

**Features**:
- Text normalization (lowercase, URL removal, whitespace)
- Duplicate removal
- Stratified train/test split (80/20)
- Data quality checks

**Input**: `data/raw.csv`
**Output**: `data/train.csv`, `data/test.csv`

### 2. Model Training (`src/train.py`)

**Purpose**: Train the spam classification model

**Features**:
- TF-IDF vectorization with optimized parameters
- Logistic Regression classifier
- Comprehensive evaluation metrics
- Model serialization

**Input**: `data/train.csv`, `data/test.csv`
**Output**: `model.pkl` (contains both model and vectorizer)

### 3. Prediction (`src/predict.py`)

**Purpose**: Classify new messages as spam or ham

**Features**:
- Model loading and caching
- Text preprocessing
- CLI interface (stdin and arguments)
- Error handling

**Input**: Text message (string)
**Output**: Classification label ('spam' or 'ham')

### 4. Web Interface (`ui/app.py`)

**Purpose**: Provide user-friendly web interface

**Features**:
- Flask REST API
- JSON and form data support
- Interactive HTML interface
- Real-time classification
- Example messages

**Endpoints**:
- `GET /` - Main interface
- `POST /classify` - Classification API

## Design Decisions

### Why Logistic Regression?

1. **Performance**: Achieves ~97% accuracy on this task
2. **Speed**: Fast training and inference
3. **Interpretability**: Easy to understand feature importance
4. **Simplicity**: Fewer hyperparameters than complex models
5. **Production-Ready**: Reliable and well-tested algorithm

### Why TF-IDF?

1. **Effective**: Captures important words while downweighting common terms
2. **Standard**: Industry-standard approach for text classification
3. **Efficient**: Fast vectorization with sparse matrices
4. **Configurable**: Many parameters to tune (n-grams, max features, etc.)

### Technology Choices

- **Python**: Industry standard for ML/NLP
- **scikit-learn**: Comprehensive, well-documented ML library
- **Flask**: Lightweight web framework, easy to deploy
- **pandas**: Efficient data manipulation
- **pytest**: Modern testing framework

## Performance Characteristics

### Model Metrics

- **Accuracy**: ~97.4% on test set
- **Precision (Spam)**: ~97.8%
- **Recall (Spam)**: ~91.3%
- **F1-Score (Spam)**: ~94.4%

### Inference Speed

- **CLI**: < 50ms per message
- **Web API**: < 100ms per request (including network)
- **Batch**: ~1000 messages/second

### Model Size

- **Serialized**: ~1.5 MB
- **Memory**: ~10 MB when loaded

## Data Flow

1. **Raw Data** → CSV file with 'label' and 'message' columns
2. **Cleaning** → Lowercase, remove URLs, normalize whitespace
3. **Splitting** → 80% train, 20% test (stratified)
4. **Vectorization** → Convert text to TF-IDF features
5. **Training** → Fit Logistic Regression
6. **Evaluation** → Test on held-out data
7. **Inference** → Preprocess → Vectorize → Predict

## Error Handling

- **Missing Model**: Clear error message with training instructions
- **Empty Input**: Validation and user-friendly error
- **Invalid Data**: Graceful degradation with logging
- **File Errors**: Descriptive messages for debugging

## Security Considerations

1. **Input Validation**: All user input is validated
2. **Resource Limits**: Text length limits to prevent abuse
3. **No Data Persistence**: Messages not stored by default
4. **Safe Dependencies**: Using well-maintained libraries

## Extensibility

The project is designed to be extended:

- **Add Models**: Easy to swap LogisticRegression for other classifiers
- **New Features**: Feature engineering pipeline is modular
- **API Expansion**: Flask app can add new endpoints
- **Languages**: Architecture supports multilingual data

## Testing Strategy

1. **Unit Tests**: Individual components (text cleaning, prediction)
2. **Integration Tests**: End-to-end pipeline
3. **Performance Tests**: Speed and accuracy benchmarks
4. **Edge Cases**: Empty input, special characters, long text

## Deployment Options

1. **Local**: Run Flask app directly
2. **Docker**: Containerize for consistent deployment
3. **Cloud**: Deploy to AWS, GCP, Azure
4. **Serverless**: Package as Lambda/Cloud Function
5. **API Gateway**: Add authentication and rate limiting

## Future Enhancements

- Multi-language support
- Deep learning models (LSTM, BERT)
- Online learning capabilities
- A/B testing framework
- Model monitoring and drift detection
- Batch processing API
- Mobile app integration

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on contributing to this project.

## License

This project is licensed under the MIT License - see [LICENSE](../LICENSE) file for details.
