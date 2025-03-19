import os
import time
import csv
from hashlib import sha256
import random

# Initialize data structures for logging
verification_times = []
challenge_iterations = []
sensitivity_levels = []
difficulty_levels = []

# Load knowledge bank and blockchain data
def load_knowledge_bank():
    knowledge_bank = {}
    with open('knowledge_bank.csv', 'r') as kb:
        reader = csv.reader(kb)
        for row in reader:
            knowledge_bank[row[0]] = row[1]  # {image_name: hash}
    return knowledge_bank

def load_blockchain():
    blockchain = []
    with open("blockchain.txt", "r") as f:
        block = {}
        for line in f:
            line = line.strip()
            if line.startswith("Block Number:"):
                block = {'Block Number': int(line.split(": ")[1])}
            elif line.startswith("Sensitivity:"):
                block['Sensitivity'] = line.split(": ")[1]
            elif line.startswith("Difficulty Level:"):
                block['Difficulty Level'] = int(line.split(": ")[1])
            elif line.startswith("Data:"):
                block['Data'] = line.split(": ")[1]
            elif line.startswith("New Hash:"):
                block['New Hash'] = line.split(": ")[1]
            elif line == "-" * 40:
                blockchain.append(block)
    return blockchain

def verify_image(image_name, knowledge_bank, blockchain):
    if image_name not in knowledge_bank:
        print(f"Image {image_name} not found in knowledge bank.")
        return None

    # Prover provides the hash for the given image
    image_hash = knowledge_bank[image_name]

    # Start verification timer
    start_time = time.time()

    # Attempt to verify with challenge iterations
    for challenge in range(1, 101):
        challenge_hash = sha256((image_hash + str(challenge)).encode()).hexdigest()
        for block in blockchain:
            if challenge_hash == block['Data']:
                # Verification success
                verification_time = time.time() - start_time
                verification_times.append(verification_time)
                challenge_iterations.append(challenge)
                sensitivity_levels.append(block['Sensitivity'])
                difficulty_levels.append(block['Difficulty Level'])

                # Additional verification using new hash
                block_data = str(block['Data']) + str(block['Difficulty Level']) + str(block['Nonce'])
                new_hash = sha256(block_data.encode()).hexdigest()
                if new_hash == block['New Hash']:
                    print(f"Verification successful for {image_name}!")
                    print(f"Verification Time: {verification_time:.2f} seconds")
                    print(f"Challenge Iterations: {challenge}")
                    return verification_time, challenge
                else:
                    print("Verification failed: Hash mismatch.")
                    return None

    print(f"Verification failed for {image_name}.")
    return None

# Load data
knowledge_bank = load_knowledge_bank()
blockchain = load_blockchain()

# Randomly choose an image for verification
image_name = random.choice(list(knowledge_bank.keys()))
verify_image(image_name, knowledge_bank, blockchain)

# Save verification data for plotting
with open('verifier_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Image", "Verification Time", "Challenge Iterations", "Sensitivity Level", "Difficulty Level"])
    for i in range(len(verification_times)):
        writer.writerow([image_name, verification_times[i], challenge_iterations[i], sensitivity_levels[i], difficulty_levels[i]])

print("Data saved to verifier_data.csv for plotting.")
