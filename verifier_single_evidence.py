import os
import csv
import random
from hashlib import sha256

# Paths to the required files
image_folder = "images"
knowledge_bank_file = "knowledge_bank.csv"
blockchain_file = "blockchain.txt"


# Function to get a random image name from the image folder
def get_random_image_name():
    images = [img for img in os.listdir(image_folder) if img.endswith((".jpg", ".jpeg", ".png"))]
    return random.choice(images) if images else None


# Function to find the hash associated with an image name in the knowledge bank
def get_image_hash_from_knowledge_bank(image_name):
    with open(knowledge_bank_file, 'r') as kb:
        reader = csv.reader(kb)
        for row in reader:
            if row[0] == image_name:
                return row[1]  # Return the associated hash value
    return None


# Function to retrieve block data from blockchain.txt
def get_block_data():
    blocks = []
    current_block = {}
    with open(blockchain_file, 'r') as bc:
        for line in bc:
            line = line.strip()
            if line.startswith("Block Number"):
                if current_block:
                    blocks.append(current_block)
                current_block = {'Block Number': line.split(": ")[1]}
            elif line.startswith("Sensitivity"):
                current_block['Sensitivity'] = line.split(": ")[1]
            elif line.startswith("Difficulty Level"):
                current_block['Difficulty Level'] = line.split(": ")[1]
            elif line.startswith("Data"):
                current_block['Data'] = line.split(": ")[1]
            elif line.startswith("Nonce"):
                current_block['Nonce'] = line.split(": ")[1]
            elif line.startswith("Previous Hash"):
                current_block['Previous Hash'] = line.split(": ")[1]
            elif line.startswith("New Hash"):
                current_block['New Hash'] = line.split(": ")[1]
            elif line == "-" * 40:
                blocks.append(current_block)
                current_block = {}
    return blocks


# Function to verify the evidence using the prover's hash and blockchain data
def verify_evidence(image_name, prover_hash):
    blocks = get_block_data()

    # Iterate over each block in the blockchain to find a matching "Data"
    for block in blocks:
        for challenge in range(1, 10001):  # Challenge range from 1 to 100
            # Generate hash for the challenge
            verifier_challenge_hash = sha256((prover_hash + str(challenge)).encode()).hexdigest()
            if verifier_challenge_hash == block['Data']:
                print(f"Data matched for image '{image_name}' at challenge {challenge}. Verifying New Hash...")

                # Verifying by reconstructing the new hash
                block_data = verifier_challenge_hash + block['Sensitivity'] + block['Difficulty Level']
                difficulty = int(block['Difficulty Level'])
                nonce = int(block['Nonce'])
                generated_hash = sha256((block_data + block['Previous Hash'] + str(nonce)).encode()).hexdigest()

                # Check if the generated hash matches the block's New Hash
                if generated_hash == block['New Hash']:
                    print("Verification Successful: New Hash matched with the blockchain record.")
                    return True
                else:
                    print("Verification Failed: New Hash did not match.")
                    return False
    print("Verification Failed: No matching data found.")
    return False


# Main verification process
if __name__ == "__main__":
    # Step 1: Verifier selects a random image name
    image_name = get_random_image_name()
    if image_name is None:
        print("No images found in the image folder.")
    else:
        print(f"Verifier selected image '{image_name}' for zero-knowledge proof request.")

        # Step 2: Prover retrieves the hash from knowledge bank
        prover_hash = get_image_hash_from_knowledge_bank(image_name)
        if prover_hash is None:
            print(f"No hash found for '{image_name}' in knowledge bank.")
        else:
            print(f"Prover provided hash: {prover_hash}")

            # Step 3: Verifier verifies the hash using the blockchain data
            verified = verify_evidence(image_name, prover_hash)
            if verified:
                print(f"Verification of '{image_name}' completed successfully.")
            else:
                print(f"Verification of '{image_name}' failed.")
