import pandas as pd

def read_any_excel(path):
    try:
        # Try Excel
        return pd.read_excel(path)
    except Exception:
        pass

    try:
        # Try CSV
        return pd.read_csv(path)
    except Exception:
        pass

    raise ValueError("File is not Excel or CSV. It may be corrupted.")

# === USE THE VALID UPLOADED FILE ===
file_path = "/mnt/data/Sample Data 2.xlsx"

df = read_any_excel(file_path)
print(df.head())
print("\nRows:", len(df))
