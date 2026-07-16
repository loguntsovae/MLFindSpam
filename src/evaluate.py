"""Evaluate the trained model on the held-out test set.

Prints precision/recall/F1 and writes a confusion-matrix figure to
docs/img/confusion.png.

Usage:
    python -m src.evaluate
"""
import pathlib
import pickle

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix


def main() -> None:
    root = pathlib.Path(__file__).resolve().parent.parent
    with open(root / "model.pkl", "rb") as f:
        data = pickle.load(f)
    model, vectorizer = data["model"], data["vectorizer"]

    test = pd.read_csv(root / "data" / "test.csv")
    X = vectorizer.transform(test["message"].fillna(""))
    y_true = test["label"]
    y_pred = model.predict(X)

    print(classification_report(y_true, y_pred, digits=3))

    cm = confusion_matrix(y_true, y_pred, labels=["ham", "spam"])
    fig, ax = plt.subplots(figsize=(4.6, 4.0), facecolor="#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    im = ax.imshow(cm, cmap="Blues")
    for (i, j), v in np.ndenumerate(cm):
        share = v / cm.sum()
        ax.text(j, i, f"{v}\n{share:.1%}", ha="center", va="center", fontsize=13,
                fontweight="bold", color="white" if v > cm.max() / 2 else "#0b0b0b")
    ax.set_xticks([0, 1], ["ham", "spam"])
    ax.set_yticks([0, 1], ["ham", "spam"])
    ax.set_xlabel("predicted")
    ax.set_ylabel("actual")
    ax.set_title("Confusion matrix — held-out test set", fontweight="bold", fontsize=11)
    fig.colorbar(im, shrink=0.8)
    out = root / "docs" / "img" / "confusion.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight", pad_inches=0.2)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
