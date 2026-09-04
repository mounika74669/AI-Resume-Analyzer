import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# ==========================================
# 1. FIND DATASET
# ==========================================

possible_paths = [
    "data/archive/Resume/Resume.csv",
    "data/Resume/Resume.csv",
    "Resume.csv"
]

csv_path = None

for path in possible_paths:
    if os.path.exists(path):
        csv_path = path
        break

if csv_path is None:
    print("❌ Resume.csv not found!")
    print("Current folder:", os.getcwd())
    print("\nPlease check that Resume.csv is inside:")
    print("data/archive/Resume/")
    exit()

print("✅ Dataset found:", csv_path)

# ==========================================
# 2. LOAD DATASET
# ==========================================

df = pd.read_csv(csv_path)

print("\nDataset loaded successfully!")
print("Number of resumes:", len(df))

print("\nColumns:")
print(df.columns.tolist())

# ==========================================
# 3. CHECK REQUIRED COLUMNS
# ==========================================

if "Resume_str" not in df.columns:
    print("❌ Resume_str column not found!")
    exit()

if "Category" not in df.columns:
    print("❌ Category column not found!")
    exit()

# Remove missing values
df = df.dropna(subset=["Resume_str", "Category"])

X = df["Resume_str"].astype(str)
y = df["Category"].astype(str)

print("\nData prepared successfully!")
print("Total usable resumes:", len(df))
print("Number of categories:", y.nunique())

# ==========================================
# 4. SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining data:", len(X_train))
print("Testing data:", len(X_test))

# ==========================================
# 5. CREATE ML MODEL
# ==========================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english",
            max_features=10000
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])

# ==========================================
# 6. TRAIN MODEL
# ==========================================

print("\nTraining model...")

model.fit(X_train, y_train)

print("✅ Model training completed!")

# ==========================================
# 7. TEST MODEL
# ==========================================

print("\nTesting model...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n==========================================")
print("MODEL ACCURACY")
print("==========================================")
print(f"{accuracy * 100:.2f}%")

print("\n==========================================")
print("CLASSIFICATION REPORT")
print("==========================================")

print(classification_report(
    y_test,
    y_pred,
    zero_division=0
))

# ==========================================
# 8. SAVE MODEL
# ==========================================

try:
    import joblib

    model_path = "resume_model.pkl"

    joblib.dump(model, model_path)

    print("\n==========================================")
    print("MODEL SAVED SUCCESSFULLY!")
    print("==========================================")
    print("Saved as:", model_path)

except ImportError:
    print("\n❌ joblib is not installed.")
    print("Run this command:")
    print("pip install joblib")

# ==========================================
# 9. TEST WITH SAMPLE RESUME
# ==========================================

sample_resume = """
Python developer with experience in machine learning,
data analysis, SQL, pandas, numpy and artificial intelligence.
"""

prediction = model.predict([sample_resume])

print("\n==========================================")
print("SAMPLE RESUME PREDICTION")
print("==========================================")

print("Predicted Category:", prediction[0])

print("\n✅ Main.py completed successfully!")