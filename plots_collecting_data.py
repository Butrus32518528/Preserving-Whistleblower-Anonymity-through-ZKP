import os
import time
import random
import csv
from hashlib import sha256
from PIL import Image
from Fingerprint import grayscale_sum
from ledger import create_new_block
import glob

# Function to resize the image
def resize_image(image_path, max_size=(800, 800)):
    image = Image.open(image_path)
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image

# Function to assign sensitivity and difficulty level
def assign_sensitivity():
    sensitivity = random.choice(["High", "Medium", "Low"])
    difficulty = {"High": 5, "Medium": 4, "Low": 3}[sensitivity]
    return sensitivity, difficulty

# Function to mine a block
def mine_block(block_data, difficulty, previous_hash):
    prefix = '0' * difficulty
    nonce = 0
    start = time.time()
    while True:
        block_content = block_data + previous_hash + str(nonce)
        block_hash = sha256(block_content.encode()).hexdigest()
        if block_hash.startswith(prefix):
            total_time = (time.time() - start)
            return block_hash, nonce, total_time
        nonce += 1

# Function to save block data to a .txt file
def save_block_to_txt(block, file_name="blockchain.txt"):
    with open(file_name, "a") as f:
        f.write(f"Block Number: {block['Block Number']}\n")
        f.write(f"Sensitivity: {block['Sensitivity']}\n")
        f.write(f"Difficulty Level: {block['Difficulty Level']}\n")
        f.write(f"Data: {block['Data']}\n")
        f.write(f"Nonce: {block['Nonce']}\n")
        f.write(f"Previous Hash: {block['Previous Hash']}\n")
        f.write(f"New Hash: {block['New Hash']}\n")
        f.write("-" * 40 + "\n")

if __name__ == "__main__":
    # Prepare logging files
    log_files = ["mining_time_difficulty.csv", "mining_time_sensitivity.csv", "total_mining_time.csv"]
    for log_file in log_files:
        if os.path.exists(log_file):
            os.remove(log_file)

    # Directory containing images
    image_folder = "images"
    processed_folder = "processed_images"

    # Create folder if it doesn't exist
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    images = glob.glob(os.path.join(image_folder, "*.jpg"))

    # Blockchain structure: a list to store each block
    blockchain = []

    previous_hash = "0"  # Initialize the first previous hash as "0"
    block_number = 1  # Starting block number
    total_mining_time = 0  # Track total mining time

    for image_path in images:
        print(f"\nProcessing image: {image_path}")

        # Resize the image and save in the processed folder
        resized_image = resize_image(image_path)
        processed_image_path = os.path.join(processed_folder, f"{os.path.basename(image_path)}")
        resized_image.save(processed_image_path)

        # Assign sensitivity and determine difficulty level
        sensitivity, difficulty = assign_sensitivity()
        print(f"Sensitivity: {sensitivity}, Difficulty Level: {difficulty}")

        # Fingerprinting: compute the grayscale intensity sum as the data
        total_intensity = grayscale_sum(processed_image_path)

        # Calculate SHA-256 hash for knowledge bank
        image_hash = sha256(str(total_intensity).encode()).hexdigest()
        with open('knowledge_bank.csv', 'a', newline='') as kb:
            writer = csv.writer(kb)
            writer.writerow([os.path.basename(processed_image_path), image_hash])

        # Generate challenge-based hash for Zero Knowledge Proof (ZKP)
        challenge = random.randint(1, 100)
        challenge_hash = sha256((image_hash + str(challenge)).encode()).hexdigest()

        # Save ZKP hash to ledger_ZKP
        with open('ledger_ZKP.csv', 'a', newline='') as zkp_ledger:
            writer = csv.writer(zkp_ledger)
            writer.writerow([block_number, challenge, challenge_hash])

        # Mining block using data, previous hash, and difficulty level
        print(f"Mining block with difficulty {difficulty}...")
        block_data = str(total_intensity) + sensitivity + str(difficulty)
        new_hash, nonce, mining_time = mine_block(block_data, difficulty, previous_hash)
        total_mining_time += mining_time  # Update total mining time

        print(f"Block mined with hash: {new_hash} (Nonce: {nonce}), Mining time: {mining_time:.2f} seconds")

        # Log data for plots
        with open("mining_time_difficulty.csv", "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([block_number, difficulty, mining_time])

        with open("mining_time_sensitivity.csv", "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([block_number, sensitivity, mining_time])

        with open("total_mining_time.csv", "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([block_number, total_mining_time])

        # Create and store the block details in the blockchain
        block = {
            'Block Number': block_number,
            'Sensitivity': sensitivity,
            'Difficulty Level': difficulty,
            'Data': challenge_hash,
            'Nonce': nonce,
            'Previous Hash': previous_hash,
            'New Hash': new_hash
        }
        blockchain.append(block)

        # Save the block data to a .txt file
        save_block_to_txt(block)

        # Update the previous hash for the next block
        previous_hash = new_hash
        block_number += 1

    print(f"\nTotal mining time for all images: {total_mining_time:.2f} seconds")
