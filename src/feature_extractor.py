"""
Enhanced feature extraction for multilingual spam detection.
Adds specific features for Russian and English spam patterns.
"""

import re
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class SpamFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Extract spam-specific features from messages.
    Works for both English and Russian text.
    """
    
    def __init__(self):
        # Russian spam keywords
        self.russian_spam_keywords = [
            'срочно', 'внимание', 'выиграли', 'поздравляем', 'приз',
            'бесплатно', 'акция', 'скидка', 'заблокирован', 'позвоните',
            'кредит', 'займ', 'одобрен', 'деньги', 'рубл', 'тысяч',
            'заработок', 'доход', 'получ', 'выплат', 'бонус'
        ]
        
        # English spam keywords
        self.english_spam_keywords = [
            'winner', 'congratulations', 'won', 'prize', 'free',
            'urgent', 'click', 'call', 'text', 'claim', 'limited',
            'offer', 'guaranteed', 'cash', 'credit', 'loan'
        ]
        
        # URL patterns
        self.url_pattern = re.compile(r'http[s]?://|www\.|\.com|\.ru|\.net|\.org')
        
        # Phone patterns (both Russian and international)
        self.russian_phone_pattern = re.compile(r'8-\d{3,4}-\d{3,4}|\+7-\d{3}-\d{3}-\d{2}-\d{2}')
        self.intl_phone_pattern = re.compile(r'\d{3,4}-\d{3,4}|\d{5,}')
        
        # Money patterns
        self.money_pattern_ru = re.compile(r'\d+\s?(руб|тыс|млн|₽)|р\.|рубл')
        self.money_pattern_en = re.compile(r'\$\d+|£\d+|€\d+|\d+\s?(dollar|pound|euro)')
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        """Extract features from text messages"""
        features = []
        
        for text in X:
            text_lower = text.lower()
            
            feature_dict = {
                # Text characteristics
                'length': len(text),
                'word_count': len(text.split()),
                'avg_word_length': np.mean([len(word) for word in text.split()]) if text else 0,
                
                # Spam indicators
                'has_url': 1 if self.url_pattern.search(text_lower) else 0,
                'has_russian_phone': 1 if self.russian_phone_pattern.search(text) else 0,
                'has_intl_phone': 1 if self.intl_phone_pattern.search(text) else 0,
                'has_money_ru': 1 if self.money_pattern_ru.search(text_lower) else 0,
                'has_money_en': 1 if self.money_pattern_en.search(text_lower) else 0,
                
                # Character patterns
                'exclamation_count': text.count('!'),
                'question_count': text.count('?'),
                'caps_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0,
                'digit_ratio': sum(1 for c in text if c.isdigit()) / len(text) if text else 0,
                
                # Keyword matching
                'russian_spam_words': sum(1 for word in self.russian_spam_keywords if word in text_lower),
                'english_spam_words': sum(1 for word in self.english_spam_keywords if word in text_lower),
                
                # Language detection (simple)
                'has_cyrillic': 1 if re.search('[а-яА-Я]', text) else 0,
                'has_latin': 1 if re.search('[a-zA-Z]', text) else 0,
                
                # Specific spam patterns
                'has_win_pattern': 1 if re.search(r'(выигра|won|winner)', text_lower) else 0,
                'has_urgent_pattern': 1 if re.search(r'(срочно|urgent|attention|внимание)', text_lower) else 0,
                'has_free_pattern': 1 if re.search(r'(бесплатно|free|даром)', text_lower) else 0,
                'has_click_pattern': 1 if re.search(r'(кликни|нажми|click|tap)', text_lower) else 0,
                'has_block_pattern': 1 if re.search(r'(заблокирован|blocked|suspend)', text_lower) else 0,
            }
            
            features.append(list(feature_dict.values()))
        
        return np.array(features)
    
    def get_feature_names(self):
        """Return feature names for interpretability"""
        return [
            'length', 'word_count', 'avg_word_length',
            'has_url', 'has_russian_phone', 'has_intl_phone',
            'has_money_ru', 'has_money_en',
            'exclamation_count', 'question_count',
            'caps_ratio', 'digit_ratio',
            'russian_spam_words', 'english_spam_words',
            'has_cyrillic', 'has_latin',
            'has_win_pattern', 'has_urgent_pattern',
            'has_free_pattern', 'has_click_pattern', 'has_block_pattern'
        ]


def add_spam_features(messages):
    """
    Helper function to extract spam features from messages.
    
    Args:
        messages: List or Series of text messages
        
    Returns:
        numpy array of extracted features
    """
    extractor = SpamFeatureExtractor()
    return extractor.fit_transform(messages)
