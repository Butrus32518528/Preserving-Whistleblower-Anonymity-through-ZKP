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
            print(f"Mining took: {total_time} seconds")
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
    # Delete the ledger and knowledge bank if they exist
    if os.path.exists('ledger.csv'):
        os.remove('ledger.csv')
    if os.path.exists('knowledge_bank.csv'):
        os.remove('knowledge_bank.csv')
    if os.path.exists('ledger_ZKP.csv'):
        os.remove('ledger_ZKP.csv')
    if os.path.exists('blockchain.txt'):
        os.remove('blockchain.txt')

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
    total_mining_time = 0  # Track cumulative mining time
    mining_times = []  # Store individual mining times

    for image_path in images:
        print(f"\nProcessing image: {image_path}")

        # Resize the image and save in the processed folder
        resized_image = resize_image(image_path)
        processed_image_path = os.path.join(processed_folder, f"{os.path.basename(image_path)}")
        resized_image.save(processed_image_path)

        # Assign sensitivity and determine difficulty level
        sensitivity, difficulty = assign_sensitivity()
        print(f"Sensitivity: {sensitivity}, Difficulty Level: {difficulty}")

        # Fingerprinting: compute the grayscale intensity sum as the image intensity
        total_intensity = grayscale_sum(processed_image_path)

        # Calculate SHA-256 hash of image intensity for knowledge bank
        image_intensity_hash = sha256(str(total_intensity).encode()).hexdigest()
        print(f"Zero knowledge data: {image_intensity_hash}")
        # Save image intensity hash to knowledge bank
        with open('knowledge_bank.csv', 'a', newline='') as kb:
            writer = csv.writer(kb)
            writer.writerow([os.path.basename(processed_image_path), image_intensity_hash])

        # Generate challenge-based hash for Zero Knowledge Proof (ZKP)
        challenge = random.randint(1, 10000)
        challenge_hash = sha256((image_intensity_hash + str(challenge)).encode()).hexdigest()

        # Save ZKP hash to ledger_ZKP
        with open('ledger_ZKP.csv', 'a', newline='') as zkp_ledger:
            writer = csv.writer(zkp_ledger)
            writer.writerow([block_number, challenge, challenge_hash])

        # Mining block using challenge_hash, previous hash, and difficulty level
        print(f"Mining block with difficulty {difficulty}...")
        block_data = challenge_hash + sensitivity + str(difficulty)
        new_hash, nonce, mining_time = mine_block(block_data, difficulty, previous_hash)
        print(f"Block mined with hash: {new_hash} (Nonce: {nonce})")

        # Update total mining time and record individual mining time
        total_mining_time += mining_time
        mining_times.append(mining_time)
        print(f"Cumulative Mining Time: {total_mining_time} seconds")

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

        # Update the ledger with the new block
        create_new_block(block_number, new_hash)

        # Update the previous hash for the next block
        previous_hash = new_hash
        block_number += 1

    # Visualize the blockchain
    print("\nBlockchain:")
    for block in blockchain:
        print(f"Block Number: {block['Block Number']}")
        print(f"  Sensitivity: {block['Sensitivity']}")
        print(f"  Difficulty Level: {block['Difficulty Level']}")
        print(f"  Data: {block['Data']}")
        print(f"  Nonce: {block['Nonce']}")
        print(f"  Previous Hash: {block['Previous Hash']}")
        print(f"  New Hash: {block['New Hash']}")
        print("-" * 40)

    # Display total mining time and mean mining time
    mean_mining_time = total_mining_time / len(mining_times) if mining_times else 0
    print(f"\nTotal Mining Time for All Blocks: {total_mining_time} seconds")
    print(f"Mean Mining Time per Block: {mean_mining_time} seconds")
