#Section 01 -import.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report
from sklearn.inspection import permutation_importance

SEED = 42
rng = np.random.default_rng(SEED)

CLASS_START_MIN = 8 * 60
LATE_THRESHOLD = CLASS_START_MIN + 5  # 08:05

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]

DATASET_PATH = Path("/content/AI in Research Workshop Dataset.csv") #Please change the path here Line no. 24
MODEL_PATH = Path("late_mlp_trained_scaled.joblib")

FEATURES = ["wake_time_min", "sleep_start_min", "screen_after_wake_min", "prep_min", "commute_min"]
LABEL = "late"


def min_to_hhmm(m: float) -> str:
    m = int(round(m)) % (24 * 60)
    return f"{m//60:02d}:{m%60:02d}"


def hhmm_to_min(hhmm: str) -> int:
    hhmm = hhmm.strip()
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def clamp(x, lo, hi):
    return max(lo, min(hi, x))

