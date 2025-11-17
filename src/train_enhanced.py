"""
Enhanced model training script for SMS Spam Classifier.
Trains a LogisticRegression model with TF-IDF vectorization and custom features.
Optimized for multilingual spam detection (English + Russian).
"""

import sys
from pathlib import Path
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import custom feature extractor
from src.feature_extractor import SpamFeatureExtractor


def train_model(train_path='data/train.csv', test_path='data/test.csv', 
                model_path='model.pkl'):
    """
    Train an enhanced spam classifier using LogisticRegression with TF-IDF and custom features.
    
    Args:
        train_path: Path to training data
        test_path: Path to test data
        model_path: Path to save trained model
    """
    print("="*60)
    print("ENHANCED MULTILINGUAL SPAM CLASSIFIER TRAINING")
    print("="*60)
    
    print("\n📊 Loading training data...")
    train_df = pd.read_csv(train_path)
    
    print("📊 Loading test data...")
    test_df = pd.read_csv(test_path)
    
    # Prepare data
    X_train = train_df['message']
    y_train = train_df['label']
    X_test = test_df['message']
    y_test = test_df['label']
    
    print(f"\n📈 Dataset Statistics:")
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")
    print(f"   Train spam ratio: {(y_train == 'spam').sum() / len(y_train):.2%}")
    print(f"   Test spam ratio: {(y_test == 'spam').sum() / len(y_test):.2%}")
    
    # Detect languages in dataset
    cyrillic_train = X_train.str.contains('[а-яА-Я]', regex=True).sum()
    cyrillic_test = X_test.str.contains('[а-яА-Я]', regex=True).sum()
    print(f"\n🌍 Language Distribution:")
    print(f"   Russian messages in train: {cyrillic_train} ({cyrillic_train/len(X_train):.1%})")
    print(f"   Russian messages in test: {cyrillic_test} ({cyrillic_test/len(X_test):.1%})")
    
    print("\n🔧 Building feature extraction pipeline...")
    
    # Create TF-IDF Vectorizer optimized for multilingual text
    tfidf_vectorizer = TfidfVectorizer(
        max_features=5000,
        min_df=1,
        max_df=0.85,
        ngram_range=(1, 3),  # Character tri-grams
        analyzer='char_wb',  # Character-based works better for Russian
        lowercase=True,
        sublinear_tf=True,  # Use log scaling for term frequency
    )
    
    # Create feature union combining TF-IDF and custom features
    feature_union = FeatureUnion([
        ('tfidf', tfidf_vectorizer),
        ('spam_features', Pipeline([
            ('extract', SpamFeatureExtractor()),
            ('scale', StandardScaler())
        ]))
    ])
    
    print("   ✓ TF-IDF vectorizer configured")
    print("   ✓ Custom spam features extractor configured")
    print("   ✓ Feature scaling configured")
    
    # Fit and transform training data
    print("\n⚙️  Extracting features from training data...")
    X_train_features = feature_union.fit_transform(X_train)
    print(f"   Feature matrix shape: {X_train_features.shape}")
    
    print("⚙️  Extracting features from test data...")
    X_test_features = feature_union.transform(X_test)
    
    print("\n🤖 Training Logistic Regression model...")
    # Train Logistic Regression with optimized parameters
    model = LogisticRegression(
        max_iter=2000,
        random_state=42,
        C=0.5,  # Regularization strength
        solver='saga',  # Best for large datasets
        class_weight='balanced',  # Handle class imbalance
        penalty='l2',
        verbose=0
    )
    
    model.fit(X_train_features, y_train)
    print("   ✓ Model training complete")
    
    # Evaluate on training set
    print("\n📊 Evaluating model performance...")
    y_train_pred = model.predict(X_train_features)
    train_accuracy = accuracy_score(y_train, y_train_pred)
    
    # Evaluate on test set
    y_test_pred = model.predict(X_test_features)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    
    # Get prediction probabilities
    y_test_proba = model.predict_proba(X_test_features)
    
    print("\n" + "="*60)
    print("MODEL PERFORMANCE")
    print("="*60)
    print(f"\n✅ Train Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
    print(f"✅ Test Accuracy:  {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    # Check for overfitting
    if train_accuracy - test_accuracy > 0.05:
        print(f"\n⚠️  Warning: Potential overfitting detected")
        print(f"   (Train-Test gap: {(train_accuracy - test_accuracy)*100:.2f}%)")
    else:
        print(f"\n✓ Good generalization (Train-Test gap: {(train_accuracy - test_accuracy)*100:.2f}%)")
    
    print("\n" + "-"*60)
    print("DETAILED CLASSIFICATION REPORT (Test Set)")
    print("-"*60)
    print(classification_report(y_test, y_test_pred, digits=4))
    
    print("-"*60)
    print("CONFUSION MATRIX")
    print("-"*60)
    cm = confusion_matrix(y_test, y_test_pred)
    print(f"\n                Predicted")
    print(f"               Ham    Spam")
    print(f"Actual Ham    {cm[0][0]:5d}  {cm[0][1]:5d}")
    print(f"       Spam   {cm[1][0]:5d}  {cm[1][1]:5d}")
    
    # Calculate specific metrics
    tn, fp, fn, tp = cm.ravel()
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    print(f"\n📈 Additional Metrics:")
    print(f"   Specificity (Ham detection): {specificity:.4f} ({specificity*100:.2f}%)")
    print(f"   Sensitivity (Spam detection): {sensitivity:.4f} ({sensitivity*100:.2f}%)")
    print(f"   False Positive Rate: {fp/(fp+tn)*100:.2f}%")
    print(f"   False Negative Rate: {fn/(fn+tp)*100:.2f}%")
    
    # Save model
    print(f"\n💾 Saving model to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump({
            'model': model,
            'vectorizer': feature_union,
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy
        }, f)
    
    print("   ✓ Model saved successfully")
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETED SUCCESSFULLY")
    print("="*60)
    print(f"\n🎯 Final Test Accuracy: {test_accuracy*100:.2f}%")
    
    if test_accuracy >= 0.98:
        print("🏆 EXCELLENT! Model achieves >98% accuracy")
    elif test_accuracy >= 0.95:
        print("🎉 GREAT! Model achieves >95% accuracy")
    elif test_accuracy >= 0.90:
        print("👍 GOOD! Model achieves >90% accuracy")
    else:
        print("⚠️  Model accuracy below 90%. Consider adding more training data.")
    
    print("\n💡 Model is ready for deployment!")
    print(f"   Use: python src/predict.py <message>")
    print(f"   Or:  python ui/app.py (for web interface)")
    
    return model, feature_union


if __name__ == "__main__":
    model, vectorizer = train_model()
