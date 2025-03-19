import csv
import hashlib
import os
import time

# Function to create or update the ledger with block number and hash
def create_or_update_ledger(block_number, block_hash, ledger_file='ledger.csv'):
    # Check if the file exists to determine if we need to write the header
    file_exists = os.path.isfile(ledger_file)

    # Open the file in append mode
    with open(ledger_file, 'a', newline='') as csvfile:
        fieldnames = ['Block Number', 'Hash']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header if the file is new
        if not file_exists:
            writer.writeheader()

        # Write the new block information
        writer.writerow({'Block Number': block_number, 'Hash': block_hash})


# Function to create a new block and add it to the ledger
def create_new_block(block_number, block_hash):
    start = time.time()
    create_or_update_ledger(block_number, block_hash)
    print(f"Block {block_number} with hash {block_hash} added to the ledger.")
    total_time = (time.time() - start)
    # print(f"Mining took: {total_time} seconds")
    return total_time


# Function to read the ledger data (block number and corresponding hash)
def read_ledger(ledger_file='ledger.csv'):
    ledger_data = {}
    try:
        with open(ledger_file, 'r') as f:
            # Use the csv.reader to manually handle the header
            reader = csv.reader(f)
            header = next(reader)  # Read the header line

            # Ensure the header is as expected
            if header != ['Block Number', 'Hash']:
                print(f"Unexpected header: {header}. Please check the CSV file.")
                return ledger_data

            for row in reader:
                # Ensure the row contains exactly 2 elements
                if len(row) == 2:
                    block_number_str, block_hash = row[0].strip(), row[1].strip()
                    # Try converting block number to integer
                    try:
                        block_number = int(block_number_str)
                        ledger_data[block_number] = block_hash
                    except ValueError:
                        print(f"Invalid block number found: '{block_number_str}'. Skipping this row.")
                else:
                    print(f"Invalid row found: {row}. Skipping this row.")
    except FileNotFoundError:
        print(f"Ledger file '{ledger_file}' not found.")
    return ledger_data



