import csv
import os
import logging
from collections import defaultdict
from tqdm import tqdm

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        filename='deduplication.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info('Logging setup complete.')

def validate_input_file(file_path):
    """Validate the input CSV file"""
    if not os.path.isfile(file_path):
        logging.error(f"File {file_path} does not exist.")
        raise FileNotFoundError(f"File {file_path} does not exist.")
    if not file_path.endswith('.csv'):
        logging.error(f"File {file_path} is not a CSV file.")
        raise ValueError(f"File {file_path} is not a CSV file.")
    logging.info(f"Input file {file_path} validated successfully.")

def remove_duplicates(input_file, output_file, columns_to_check):
    """Remove duplicate records from a CSV file"""
    seen_data = defaultdict(list)
    
    validate_input_file(input_file)
    
    try:
        with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row in tqdm(reader, desc="Processing rows"):
                key = tuple(row[col] for col in columns_to_check)
                if key not in seen_data:
                    writer.writerow(row)
                    seen_data[key] = row
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
    else:
        logging.info(f"Duplicates removed and saved to {output_file}")
        print(f"Duplicates removed and saved to {output_file}")

def main():
    setup_logging()
    input_file = 'iput.csv'
    output_file = 'output.csv'
    columns_to_check = ['ln', 'dob', 'gn', 'fn']  # Specify the columns to check for duplicates
    logging.info("Starting deduplication process")
    remove_duplicates(input_file, output_file, columns_to_check)
    logging.info("Deduplication process completed successfully")

if __name__ == '__main__':
    main()
