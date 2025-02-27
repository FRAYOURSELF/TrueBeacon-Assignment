import os
import zipfile
import csv
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database import engine, ticks, bhavcopy

def ingest_ticks_data(zip_path: str):
    # Extract zip files
    extracted_path = 'data/extracted'
    os.makedirs(extracted_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as main_zip:
        main_zip.extractall(extracted_path)

    # Extract nested zips and process the first CSV file only
    first_csv_processed = False
    with Session(engine) as session:
        for root, dirs, files in os.walk(extracted_path):
            for file in files:
                if file.endswith('.zip'):
                    nested_zip_path = os.path.join(root, file)
                    with zipfile.ZipFile(nested_zip_path, 'r') as nested_zip:
                        nested_zip.extractall(root)

            # Process only the first CSV file
            for file in files:
                if file.endswith('.csv') and not first_csv_processed:
                    csv_path = os.path.join(root, file)
                    with open(csv_path, mode='r', encoding='ISO-8859-1') as f:
                        reader = csv.reader(f)
                        next(reader)  # Skip the header row
                        for i, row in enumerate(reader):
                            session.execute(ticks.insert().values(
                                symbol=row[0],
                                timestamp=f"{row[1]} {row[2]}",
                                price=float(row[3]),
                                quantity=int(row[8])
                            ))
                    first_csv_processed = True
        session.commit()

def ingest_bhavcopy_data(zip_path: str):
    # Extraction path
    extracted_path = 'data/extracted_bhavcopy'
    nested_path = os.path.join(extracted_path, 'nested')

    # Step 1: Extract main ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_path)
    print(f"Extracted {zip_path} to {extracted_path}")

    # Step 2: Select any one ZIP file inside extracted_path
    nested_zip = None
    for file in os.listdir(extracted_path):
        if file.endswith('.zip'):
            nested_zip = os.path.join(extracted_path, file)
            break

    if not nested_zip:
        print("No ZIP file found inside extracted_bhavcopy.")
        return

    # Step 3: Extract the selected ZIP into 'nested'
    with zipfile.ZipFile(nested_zip, 'r') as zip_ref:
        zip_ref.extractall(nested_path)
    print(f"Extracted {nested_zip} to {nested_path}")

    # Step 4: Pick any one CSV inside the nested folder
    csv_file = None
    for file in os.listdir(nested_path):
        if file.endswith('.csv'):
            csv_file = os.path.join(nested_path, file)
            break

    if not csv_file:
        print("No CSV file found inside nested.")
        return

    # Step 5: Process the first 100 rows of the CSV file
    with Session(engine) as session:
        with open(csv_file, mode='r', encoding='ISO-8859-1') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for i, row in enumerate(reader):
                try:
                    session.execute(bhavcopy.insert().values(
                        symbol=row[0],
                        close_price=float(row[5]),
                        timestamp=datetime.strptime(row[10], '%d-%b-%Y')
                    ))
                except Exception as e:
                    print(f"Error processing row {i}: {e}")
        session.commit()
        print("Bhavcopy data ingested successfully!")