# MLFindSpam

[![CI](https://github.com/loguntsovae/MLFindSpam/actions/workflows/ci.yml/badge.svg)](https://github.com/loguntsovae/MLFindSpam/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

SMS spam classifier using Logistic Regression + TF-IDF. Multilingual (English + Russian). ~97–98% accuracy on the SMS Spam Collection dataset.

## How it works

- **Preprocessing** — lowercasing, URL stripping, whitespace normalisation
- **Vectorisation** — TF-IDF with character n-grams `(1, 3)`, 5 000 features, tuned for multilingual text
- **Classifier** — `sklearn.linear_model.LogisticRegression` (liblinear, L2)
- **Web UI** — Flask app at `localhost:5001` for interactive classification

## Quick start

```bash
pip install -r requirements.txt
make all          # prepare data → train model → run tests
```

Classify from the command line:

```bash
python src/predict.py "WINNER! You won $1000, call now!"
# → spam

python src/predict.py "Hey, are we still meeting at 3?"
# → ham
```

Or launch the web UI:

```bash
make run-ui       # open http://localhost:5001
```

## Project structure

```
src/
  prepare.py             # data cleaning + train/test split
  train.py               # model training + evaluation
  predict.py             # inference
  merge_russian_data.py  # extend dataset with Russian messages
data/
  raw.csv                # SMS Spam Collection (5 574 messages)
  russian_messages.csv   # additional Russian spam/ham examples
tests/
  test_predict.py        # pytest suite
ui/
  app.py                 # Flask web app
  templates/index.html
docs/                    # extended documentation
```

## Accuracy

| Metric | Value |
|---|---|
| Test accuracy | ~97–98% |
| Precision (spam) | ~0.98 |
| Recall (spam) | ~0.91–0.96 |
| F1 (spam) | ~0.94–0.97 |

## Russian language support

Merge the Russian dataset before training to enable multilingual detection:

```bash
make russian-train    # merge Russian data + retrain
python src/predict.py "СРОЧНО! Вы выиграли iPhone!"  # → spam
```

## License

MIT
