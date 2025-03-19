import os
import csv
import random
import time
from hashlib import sha256
import matplotlib.pyplot as plt

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
    for block in blocks:
        for challenge in range(1, 10001):  # Challenge range from 1 to 10000
            verifier_challenge_hash = sha256((prover_hash + str(challenge)).encode()).hexdigest()
            if verifier_challenge_hash == block['Data']:
                # Verifying by reconstructing the new hash
                block_data = verifier_challenge_hash + block['Sensitivity'] + block['Difficulty Level']
                difficulty = int(block['Difficulty Level'])
                nonce = int(block['Nonce'])
                generated_hash = sha256((block_data + block['Previous Hash'] + str(nonce)).encode()).hexdigest()

                if generated_hash == block['New Hash']:
                    return True  # Verification successful
    return False  # Verification failed


# Main verification process
if __name__ == "__main__":
    verification_times = []
    successful_verifications = 0
    unsuccessful_verifications = 0
    total_verification_time = 0

    images = [img for img in os.listdir(image_folder) if img.endswith((".jpg", ".jpeg", ".png"))]

    if not images:
        print("No images found in the image folder.")
    else:
        for image_name in images:
            print(f"\nVerifier selected image '{image_name}' for verification.")

            # Step 2: Prover retrieves the hash from knowledge bank
            prover_hash = get_image_hash_from_knowledge_bank(image_name)
            if prover_hash is None:
                print(f"No hash found for '{image_name}' in knowledge bank.")
                unsuccessful_verifications += 1
                verification_times.append(0)  # Add 0 for unverified image
                continue

            print(f"Prover provided hash: {prover_hash}")

            # Step 3: Verifier verifies the hash using the blockchain data
            start_time = time.time()
            verified = verify_evidence(image_name, prover_hash)
            verification_time = time.time() - start_time
            verification_times.append(verification_time)
            total_verification_time += verification_time

            if verified:
                print(f"Verification of '{image_name}' completed successfully.")
                successful_verifications += 1
            else:
                print(f"Verification of '{image_name}' failed.")
                unsuccessful_verifications += 1

        # Calculate mean verification time
        mean_verification_time = total_verification_time / len(verification_times)

        # Display summary
        print("\nSummary:")
        print(f"Total Verification Time: {total_verification_time:.2f} seconds")
        print(f"Number of Successfully Verified Images: {successful_verifications}")
        print(f"Number of Unsuccessfully Verified Images: {unsuccessful_verifications}")
        print(f"Mean Verification Time per Image: {mean_verification_time:.2f} seconds")

        # Plot verification times
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(verification_times)), verification_times, color='skyblue', label='Verification Time')
        plt.axhline(y=mean_verification_time, color='red', linestyle='--',
                    label=f'Mean Time ({mean_verification_time:.2f}s)')
        plt.xlabel("Image Index")
        plt.ylabel("Verification Time (seconds)")
        plt.title("Verification Time per Image with Mean Time")
        plt.legend()
        plt.show()
