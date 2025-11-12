import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

class DeepCleaner:
    def __init__(self):
        self.cleaner = IsolationForest(contamination=0.02, random_state=42)

    def clean(self, df, numeric_cols=None):
        """AI-alapú anomália-szűrés"""
        if numeric_cols is None:
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if len(numeric_cols) < 2:
            return df  # nincs elég adat a tisztításhoz
        try:
            mask = self.cleaner.fit_predict(df[numeric_cols])
            clean_df_
