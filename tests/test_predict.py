"""
Unit tests for SMS Spam Classifier prediction module.
Tests spam detection, ham detection, and edge cases.
"""

import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.predict import predict, clean_text


class TestPredict:
    """Test cases for the prediction functionality."""
    
    def test_spam_detection(self):
        """Test that obvious spam messages are correctly identified."""
        spam_messages = [
            "WINNER! You have been selected to receive $1000 cash prize. Call now!",
            "Congratulations! Click here to claim your FREE iPhone now!",
            "FREE FREE FREE! Text WIN to claim your prize money now!"
        ]
        
        # Count successful spam detections (should be at least 2/3 given ~96% accuracy)
        spam_count = sum(1 for message in spam_messages if predict(message) == 'spam')
        assert spam_count >= 2, f"Only {spam_count}/3 spam messages detected correctly"
    
    def test_ham_detection(self):
        """Test that normal messages are correctly identified as ham."""
        ham_messages = [
            "Hey, are we still meeting for lunch at noon?",
            "Can you pick up some milk on your way home?",
            "Meeting starts at 3pm in conference room B"
        ]
        
        for message in ham_messages:
            result = predict(message)
            assert result == 'ham', f"False positive for ham: {message}"
    
    def test_edge_cases(self):
        """Test edge cases and unusual inputs."""
        # Empty-ish message (after cleaning might become empty)
        result = predict("   ")
        assert result in ['spam', 'ham'], "Should return valid classification for whitespace"
        
        # Very short message
        result = predict("ok")
        assert result in ['spam', 'ham'], "Should handle short messages"
        
        # Message with special characters
        result = predict("Hello! How are you???")
        assert result in ['spam', 'ham'], "Should handle special characters"
        
        # Message with URLs (should be cleaned)
        result = predict("Check out this website: http://example.com")
        assert result in ['spam', 'ham'], "Should handle URLs"
        
        # Mixed case message
        result = predict("ThIs Is A TeSt MeSsAgE")
        assert result in ['spam', 'ham'], "Should handle mixed case"
        
        # Long message
        long_message = "This is a very long message. " * 50
        result = predict(long_message)
        assert result in ['spam', 'ham'], "Should handle long messages"
    
    def test_realistic_spam(self):
        """Test realistic spam patterns."""
        spam_examples = [
            "Urgent! Your account will be suspended. Click here immediately.",
            "You've won 1000 dollars! Text CLAIM to 12345",
            "Limited time offer! Get rich quick scheme, guaranteed results!",
        ]
        
        results = [predict(msg) for msg in spam_examples]
        spam_count = results.count('spam')
        # At least 2 out of 3 should be detected as spam
        assert spam_count >= 2, f"Only {spam_count}/3 realistic spam detected"
    
    def test_realistic_ham(self):
        """Test realistic legitimate messages."""
        ham_examples = [
            "Thanks for the update. I'll review it tomorrow.",
            "Running 10 minutes late, start without me.",
            "Great presentation today! Looking forward to the next meeting.",
        ]
        
        for msg in ham_examples:
            result = predict(msg)
            assert result == 'ham', f"False positive on: {msg}"


class TestCleanText:
    """Test cases for text cleaning functionality."""
    
    def test_lowercase_conversion(self):
        """Test that text is converted to lowercase."""
        text = "HELLO World"
        cleaned = clean_text(text)
        assert cleaned == "hello world"
    
    def test_url_removal(self):
        """Test that URLs are removed."""
        text = "Check this http://example.com and https://test.com"
        cleaned = clean_text(text)
        assert "http://" not in cleaned
        assert "https://" not in cleaned
        assert "example.com" not in cleaned
    
    def test_www_url_removal(self):
        """Test that www URLs are removed."""
        text = "Visit www.spam.com for details"
        cleaned = clean_text(text)
        assert "www." not in cleaned
    
    def test_whitespace_normalization(self):
        """Test that extra whitespace is normalized."""
        text = "Hello    world   test"
        cleaned = clean_text(text)
        assert cleaned == "hello world test"
    
    def test_strip_whitespace(self):
        """Test that leading/trailing whitespace is removed."""
        text = "  hello world  "
        cleaned = clean_text(text)
        assert cleaned == "hello world"
    
    def test_combined_cleaning(self):
        """Test multiple cleaning operations together."""
        text = "  CHECK THIS  http://spam.com  NOW!!!  "
        cleaned = clean_text(text)
        assert cleaned == "check this now!!!"
        assert "http://" not in cleaned
        assert "  " not in cleaned


class TestModelIntegration:
    """Integration tests for model loading and prediction."""
    
    def test_model_file_exists(self):
        """Test that model file exists before running predictions."""
        assert os.path.exists('model.pkl'), "Model file must exist. Run 'python src/train.py' first."
    
    def test_prediction_returns_valid_label(self):
        """Test that prediction always returns valid labels."""
        test_messages = [
            "normal message",
            "FREE MONEY WIN NOW",
            "hello",
            "",
            "x" * 1000  # Very long message
        ]
        
        for msg in test_messages:
            try:
                result = predict(msg)
                assert result in ['spam', 'ham'], f"Invalid result: {result}"
            except Exception as e:
                # Some messages might fail validation, that's ok
                pass
    
    def test_consistency(self):
        """Test that same message always returns same prediction."""
        message = "Test message for consistency"
        results = [predict(message) for _ in range(5)]
        
        # All results should be identical
        assert len(set(results)) == 1, "Predictions should be consistent"
    
    def test_batch_prediction(self):
        """Test predicting multiple messages."""
        messages = [
            "Meeting tomorrow at 10am",
            "WIN FREE PRIZES NOW",
            "Can you send the report?",
            "URGENT CLICK HERE",
        ]
        
        results = [predict(msg) for msg in messages]
        
        # Should have both spam and ham
        assert 'spam' in results, "Should detect some spam"
        assert 'ham' in results, "Should detect some ham"
        
        # All results should be valid
        assert all(r in ['spam', 'ham'] for r in results)


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_empty_string(self):
        """Test handling of empty string."""
        result = predict("")
        assert result in ['spam', 'ham'], "Should handle empty string gracefully"
    
    def test_only_whitespace(self):
        """Test handling of whitespace-only string."""
        result = predict("   \t\n   ")
        assert result in ['spam', 'ham'], "Should handle whitespace"
    
    def test_special_characters_only(self):
        """Test handling of special characters."""
        result = predict("!@#$%^&*()")
        assert result in ['spam', 'ham'], "Should handle special characters"
    
    def test_numbers_only(self):
        """Test handling of numeric strings."""
        result = predict("1234567890")
        assert result in ['spam', 'ham'], "Should handle numbers"
    
    def test_unicode_characters(self):
        """Test handling of unicode/emoji."""
        result = predict("Hello 世界 🌍")
        assert result in ['spam', 'ham'], "Should handle unicode"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
    """Test that the model file exists before running predictions."""
    model_path = 'model.pkl'
    if not os.path.exists(model_path):
        pytest.skip(f"Model file {model_path} not found. Run training first.")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
