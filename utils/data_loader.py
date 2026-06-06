import pandas as pd

def load_data():
    return pd.read_csv(
        "data/student_placement_prediction_dataset_2026[1].csv"
    )
