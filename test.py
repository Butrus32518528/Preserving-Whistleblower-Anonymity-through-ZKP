# import os
# import csv
# import random
# import time
# from hashlib import sha256
# import matplotlib.pyplot as plt
#
# # Paths to the required files
# image_folder = "images"
# knowledge_bank_file = "knowledge_bank.csv"
# blockchain_file = "blockchain.txt"
#
# # Function to get a random image name from the image folder
# def get_random_image_name():
#     images = [img for img in os.listdir(image_folder) if img.endswith((".jpg", ".jpeg", ".png"))]
#     return random.choice(images) if images else None
#
# # Function to find the hash associated with an image name in the knowledge bank
# def get_image_hash_from_knowledge_bank(image_name):
#     with open(knowledge_bank_file, 'r') as kb:
#         reader = csv.reader(kb)
#         for row in reader:
#             if row[0] == image_name:
#                 return row[1]  # Return the associated hash value
#     return None
#
# # Function to retrieve block data from blockchain.txt
# def get_block_data():
#     blocks = []
#     current_block = {}
#     with open(blockchain_file, 'r') as bc:
#         for line in bc:
#             line = line.strip()
#             if line.startswith("Block Number"):
#                 if current_block:
#                     blocks.append(current_block)
#                 current_block = {'Block Number': line.split(": ")[1]}
#             elif line.startswith("Sensitivity"):
#                 current_block['Sensitivity'] = line.split(": ")[1]
#             elif line.startswith("Difficulty Level"):
#                 current_block['Difficulty Level'] = line.split(": ")[1]
#             elif line.startswith("Data"):
#                 current_block['Data'] = line.split(": ")[1]
#             elif line.startswith("Nonce"):
#                 current_block['Nonce'] = line.split(": ")[1]
#             elif line.startswith("Previous Hash"):
#                 current_block['Previous Hash'] = line.split(": ")[1]
#             elif line.startswith("New Hash"):
#                 current_block['New Hash'] = line.split(": ")[1]
#             elif line == "-" * 40:
#                 blocks.append(current_block)
#                 current_block = {}
#     return blocks
#
# # Function to verify evidence with variable challenge range
# def verify_evidence(prover_hash, challenge_limit):
#     blocks = get_block_data()
#     for block in blocks:
#         for challenge in range(1, challenge_limit + 1):
#             verifier_challenge_hash = sha256((prover_hash + str(challenge)).encode()).hexdigest()
#             if verifier_challenge_hash == block['Data']:
#                 block_data = verifier_challenge_hash + block['Sensitivity'] + block['Difficulty Level']
#                 nonce = int(block['Nonce'])
#                 generated_hash = sha256((block_data + block['Previous Hash'] + str(nonce)).encode()).hexdigest()
#                 if generated_hash == block['New Hash']:
#                     return True  # Verification successful
#     return False  # Verification failed
#
# # Main verification process
# if __name__ == "__main__":
#     images = [img for img in os.listdir(image_folder) if img.endswith((".jpg", ".jpeg", ".png"))]
#
#     if not images:
#         print("No images found in the image folder.")
#     else:
#         success_counts = []
#         failure_counts = []
#         challenge_reductions = []
#
#         # Loop through challenge reduction percentages (0% to 100%)
#         for reduction in range(0, 101, 10):
#             challenge_limit = int(10000 * (1 - reduction / 100))
#             print(f"\nTesting with challenge limit reduced by {reduction}% (Limit: {challenge_limit})")
#
#             successful_verifications = 0
#             unsuccessful_verifications = 0
#
#             for image_name in images:
#                 prover_hash = get_image_hash_from_knowledge_bank(image_name)
#                 if prover_hash is None:
#                     unsuccessful_verifications += 1
#                     continue
#
#                 verified = verify_evidence(prover_hash, challenge_limit)
#                 if verified:
#                     successful_verifications += 1
#                 else:
#                     unsuccessful_verifications += 1
#
#             success_counts.append(successful_verifications)
#             failure_counts.append(unsuccessful_verifications)
#             challenge_reductions.append(challenge_limit)
#
#             print(f"Successful Verifications: {successful_verifications}")
#             print(f"Unsuccessful Verifications: {unsuccessful_verifications}")
#
#         # Plotting the results
#         fig, ax1 = plt.subplots(figsize=(12, 6))
#
#         ax1.plot(challenge_reductions, success_counts, color='green', label="Successful Verifications")
#         ax1.set_xlabel("Challenge Range Limit")
#         ax1.set_ylabel("Successful Verifications", color='green')
#         ax1.tick_params(axis='y', labelcolor='green')
#
#         ax2 = ax1.twinx()
#         ax2.plot(challenge_reductions, failure_counts, color='red', label="Unsuccessful Verifications")
#         ax2.set_ylabel("Unsuccessful Verifications", color='red')
#         ax2.tick_params(axis='y', labelcolor='red')
#
#         fig.suptitle("Verification Success and Failure Rates with Decreasing Challenge Range")
#         ax1.legend(loc='upper left')
#         ax2.legend(loc='upper right')
#         plt.show()

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

# Function to verify evidence with variable challenge range
def verify_evidence(prover_hash, challenge_limit):
    blocks = get_block_data()
    for block in blocks:
        for challenge in range(1, challenge_limit + 1):
            verifier_challenge_hash = sha256((prover_hash + str(challenge)).encode()).hexdigest()
            if verifier_challenge_hash == block['Data']:
                block_data = verifier_challenge_hash + block['Sensitivity'] + block['Difficulty Level']
                nonce = int(block['Nonce'])
                generated_hash = sha256((block_data + block['Previous Hash'] + str(nonce)).encode()).hexdigest()
                if generated_hash == block['New Hash']:
                    return True  # Verification successful
    return False  # Verification failed

# Main verification process
if __name__ == "__main__":
    images = [img for img in os.listdir(image_folder) if img.endswith((".jpg", ".jpeg", ".png"))]

    if not images:
        print("No images found in the image folder.")
    else:
        success_counts = []
        failure_counts = []
        challenge_reductions = []

        # Loop through challenge reduction percentages (0% to 100%)
        for reduction in range(0, 101, 10):
            challenge_limit = int(10000 * (1 - reduction / 100))
            print(f"\nTesting with challenge limit reduced by {reduction}% (Limit: {challenge_limit})")

            successful_verifications = 0
            unsuccessful_verifications = 0

            for image_name in images:
                prover_hash = get_image_hash_from_knowledge_bank(image_name)
                if prover_hash is None:
                    unsuccessful_verifications += 1
                    continue

                verified = verify_evidence(prover_hash, challenge_limit)
                if verified:
                    successful_verifications += 1
                else:
                    unsuccessful_verifications += 1

            success_counts.append(successful_verifications)
            failure_counts.append(unsuccessful_verifications)
            challenge_reductions.append(challenge_limit)

            print(f"Successful Verifications: {successful_verifications}")
            print(f"Unsuccessful Verifications: {unsuccessful_verifications}")

        # Plotting the successful verifications
        plt.figure(figsize=(10, 5))
        plt.plot(challenge_reductions, success_counts, marker='*', color='green', label="Successful Verifications")
        plt.xlabel("Challenge Range Limit")
        plt.ylabel("Number of Successful Verifications")
        #plt.title("Successful Verifications with Decreasing Challenge Range")
        plt.legend()
        plt.grid(True)

        # Show the plot for successful verifications
        plt.show()

        # Plotting the unsuccessful verifications
        plt.figure(figsize=(10, 5))
        plt.plot(challenge_reductions, failure_counts, marker='*', color='red', label="Unsuccessful Verifications")
        plt.xlabel("Challenge Range Limit")
        plt.ylabel("Number of Unsuccessful Verifications")
        #plt.title("Unsuccessful Verifications with Decreasing Challenge Range")
        plt.legend()
        plt.grid(True)

        # Show the plot for unsuccessful verifications
        plt.show()
