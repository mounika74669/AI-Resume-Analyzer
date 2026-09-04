 import pandas as pd
import os

print("AI Resume Analyzer - Model Training")

file_path = "data/archive/Resume/Resume.csv"

print("Checking file:")
print(file_path)

if os.path.exists(file_path):
    print("Resume.csv found!")

    df = pd.read_csv(file_path)

    print("\nDataset loaded successfully!")
    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

else:
    print("\nERROR: Resume.csv not found!")
    print("Current folder:", os.getcwd())