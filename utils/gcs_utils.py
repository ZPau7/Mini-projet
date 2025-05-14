import os
from google.cloud import storage
import pandas as pd
from io import StringIO
import csv

BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
FILE_NAME = os.getenv("GCS_FILE_NAME", "data.csv")

def get_gcs_client():
    return storage.Client()

def detect_separator(csv_text):
    try:
        sample = csv_text.splitlines()[0]
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect.delimiter
    except Exception:
        return ','  # fallback

def read_data():
    try:
        client = get_gcs_client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(FILE_NAME)
        data = blob.download_as_text()

        separator = detect_separator(data)
        df = pd.read_csv(StringIO(data), sep=separator)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error reading data: {e}")
        return []

def append_data(new_row):
    try:
        client = get_gcs_client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(FILE_NAME)

        if blob.exists():
            existing_data = blob.download_as_text()
            separator = detect_separator(existing_data)
            df = pd.read_csv(StringIO(existing_data), sep=separator)
        else:
            df = pd.DataFrame()

        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)

        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')

    except Exception as e:
        print(f"Error appending data: {e}")
