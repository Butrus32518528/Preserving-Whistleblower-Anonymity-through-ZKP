import os
import csv
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from hashlib import sha256

# Paths to the required files
image_folder = "images"
knowledge_bank_file = "knowledge_bank.csv"
blockchain_file = "blockchain.txt"


# Function to get all image names from the image folder
def get_all_image_names():
    return [img for img in os.listdir(image_folder) if img.endswith((".jpg", ".jpeg", ".png"))]


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
                block_data = verifier_challenge_hash + block['Sensitivity'] + block['Difficulty Level']
                difficulty = int(block['Difficulty Level'])
                nonce = int(block['Nonce'])
                generated_hash = sha256((block_data + block['Previous Hash'] + str(nonce)).encode()).hexdigest()
                if generated_hash == block['New Hash']:
                    return True
    return False


# Main verification process
if __name__ == "__main__":
    image_names = get_all_image_names()
    if not image_names:
        print("No images found in the image folder.")
    else:
        verification_times = []

        for image_name in image_names:
            prover_hash = get_image_hash_from_knowledge_bank(image_name)
            if prover_hash is None:
                print(f"No hash found for '{image_name}' in knowledge bank.")
                continue

            start_time = time.time()
            verified = verify_evidence(image_name, prover_hash)
            end_time = time.time()
            verification_time = end_time - start_time
            verification_times.append(verification_time)

            if verified:
                print(f"Verification of '{image_name}' completed successfully in {verification_time:.4f} seconds.")
            else:
                print(f"Verification of '{image_name}' failed in {verification_time:.4f} seconds.")

        # Calculate mean verification time
        mean_verification_time = np.mean(verification_times)
        print(f"\nMean Verification Time: {mean_verification_time:.4f} seconds")

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(verification_times)), verification_times, color='skyblue', label="Verification Time (s)")
        plt.axhline(mean_verification_time, color='red', linestyle='--',
                    label=f"Mean Time: {mean_verification_time:.4f}s")
        plt.xlabel("Image Index")
        plt.ylabel("Verification Time (seconds)")
        plt.title("Verification Time for Each Image with Mean Time")
        plt.legend()
        plt.show()
