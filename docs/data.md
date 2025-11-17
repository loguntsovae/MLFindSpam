# Data Documentation

## Dataset Overview

### Source

**SMS Spam Collection Dataset**
- Source: UCI Machine Learning Repository
- URL: http://www.dt.fee.unicamp.br/~tiago/smsspamcollection/
- License: Public Domain
- Size: 5,574 messages

### Description

The SMS Spam Collection is a public dataset of SMS messages tagged as spam or legitimate (ham). It was collected for research purposes and contains real messages donated by users.

### Statistics

- **Total Messages**: 5,574
- **Spam Messages**: 747 (13.4%)
- **Ham Messages**: 4,827 (86.6%)
- **Average Message Length**: ~80 characters
- **Languages**: Primarily English

### Class Distribution

The dataset is imbalanced, with spam representing only ~13% of messages. This reflects real-world distributions where spam is relatively rare.

```
Ham:  ████████████████████████████████████ 86.6%
Spam: █████                                13.4%
```

## Data Format

### Raw Data (`data/raw.csv`)

CSV file with the following columns:

| Column | Description | Type | Example |
|--------|-------------|------|---------|
| `v1` | Label | string | 'ham' or 'spam' |
| `v2` | Message | string | 'Hey how are you?' |

**Note**: The raw CSV may contain additional columns (v3, v4, v5) which are mostly empty and not used.

### Processed Data

After running `src/prepare.py`, the data is split into:

**`data/train.csv`** (80% of data)
- Used for training the model
- ~4,459 messages
- Maintains class distribution

**`data/test.csv`** (20% of data)
- Used for evaluation only
- ~1,115 messages
- Never seen during training

Both files have standardized columns:

| Column | Description | Type |
|--------|-------------|------|
| `label` | Class label | string ('ham' or 'spam') |
| `message` | Cleaned text | string |

## Data Preprocessing

### Text Cleaning Pipeline

The `clean_text()` function in `src/prepare.py` applies the following transformations:

1. **Lowercase Conversion**
   ```python
   "Hello World!" → "hello world!"
   ```

2. **URL Removal**
   ```python
   "Visit http://spam.com now" → "visit  now"
   ```

3. **Whitespace Normalization**
   ```python
   "hello    world" → "hello world"
   ```

4. **Trim Leading/Trailing Spaces**
   ```python
   "  hello world  " → "hello world"
   ```

### Data Quality Steps

1. **Duplicate Removal**: Messages appearing multiple times are removed
2. **Empty Message Removal**: Messages that become empty after cleaning are removed
3. **Validation**: Ensures all required columns are present

### Train/Test Split

- **Method**: Stratified split using scikit-learn's `train_test_split`
- **Ratio**: 80% training, 20% testing
- **Random Seed**: 42 (for reproducibility)
- **Stratification**: Maintains class distribution in both sets

## Example Messages

### Spam Examples

```
"WINNER!! You have been chosen to receive a $1000 cash prize! Call now!"

"FREE entry in 2 a weekly competition to win FA Cup final tickets. Text FA to 87121"

"XXXMobileMovieClub: To use your credit, click the WAP link in the next txt message"
```

### Ham Examples

```
"Hey, are we still meeting for lunch at noon?"

"Can you pick up some milk on your way home?"

"Meeting rescheduled to 3pm tomorrow. Conference room B."
```

## Data Characteristics

### Message Length Distribution

| Percentile | Length (characters) |
|------------|-------------------|
| 25% | 36 |
| 50% (median) | 62 |
| 75% | 122 |
| Max | 910 |

### Common Spam Indicators

Based on exploratory analysis, spam messages often contain:

- **Prizes/Winnings**: "WIN", "PRIZE", "WINNER", "$$$"
- **Urgency**: "NOW", "URGENT", "IMMEDIATELY", "TODAY"
- **Capitalization**: Excessive use of ALL CAPS
- **Links**: URLs and shortened links
- **Phone Numbers**: Premium rate numbers
- **Free Offers**: "FREE", "CLAIM", "GUARANTEED"

### Common Ham Patterns

Legitimate messages typically:

- Use conversational language
- Are shorter and more personal
- Contain names and specific references
- Have proper spelling and grammar
- Don't use excessive punctuation (!!!)

## Data Loading

### Using the Dataset

```python
import pandas as pd

# Load raw data
df = pd.read_csv('data/raw.csv', encoding='latin-1')
df = df[['v1', 'v2']]
df.columns = ['label', 'message']

# Load prepared data
train_df = pd.read_csv('data/train.csv')
test_df = pd.read_csv('data/test.csv')
```

## Data Privacy

- All messages in this dataset are publicly available
- Personal information has been anonymized
- No sensitive data is included
- Safe for research and educational use

## Limitations

1. **Language**: Primarily English messages
2. **Time Period**: Collected in 2012, may not reflect current spam patterns
3. **Geographic**: Mostly from UK and Singapore
4. **Imbalance**: Only 13% spam messages
5. **Static**: No temporal information or metadata

## Data Augmentation Opportunities

For future improvements, consider:

- Synonym replacement
- Back-translation
- Paraphrasing
- Oversampling minority class (SMOTE)
- Synthetic message generation

## References

- Almeida, T.A., Gómez Hidalgo, J.M., Yamakami, A. (2011). Contributions to the Study of SMS Spam Filtering: New Collection and Results. Proceedings of the 11th ACM Symposium on Document Engineering.
- UCI Machine Learning Repository: https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection
