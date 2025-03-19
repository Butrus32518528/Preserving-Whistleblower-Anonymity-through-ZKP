import os
import time
import random
import csv
from hashlib import sha256
from PIL import Image
from Fingerprint import grayscale_sum
from ledger import create_new_block
import glob
import matplotlib.pyplot as plt

# Function to resize the image
def resize_image(image_path, max_size=(800, 800)):
    image = Image.open(image_path)
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image

# Function to assign sensitivity and difficulty level based on specific ratios
def assign_sensitivity(ratio):
    sensitivity_choices = ["High"] * int(ratio[0] * 100) + \
                          ["Medium"] * int(ratio[1] * 100) + \
                          ["Low"] * int(ratio[2] * 100)
    sensitivity = random.choice(sensitivity_choices)
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

# Sensitivity ratios to be tested
ratios = [
    (0, 0, 1),     # 0% High, 0% Medium, 100% Low
    (0, 1, 0),     # 0% High, 100% Medium, 0% Low
    (1, 0, 0),     # 100% High, 0% Medium, 0% Low
    (0.25, 0.25, 0.5),   # 25% High, 25% Medium, 50% Low
    (0.25, 0.5, 0.25),   # 25% High, 50% Medium, 25% Low
    (0.5, 0.25, 0.25),   # 50% High, 25% Medium, 25% Low
    (0.33, 0.33, 0.33)   # 33% High, 33% Medium, 33% Low
]

# Main function to process images with each sensitivity ratio
def process_images_with_ratios(images):
    ratio_mining_times = []

    for ratio in ratios:
        print(f"\nProcessing with sensitivity ratio: High={ratio[0]}, Medium={ratio[1]}, Low={ratio[2]}")
        previous_hash = "0"
        block_number = 1
        total_mining_time = 0

        for image_path in images:
            # Resize the image
            resized_image = resize_image(image_path)
            processed_image_path = os.path.join(processed_folder, f"{os.path.basename(image_path)}")
            resized_image.save(processed_image_path)

            # Assign sensitivity and determine difficulty level
            sensitivity, difficulty = assign_sensitivity(ratio)

            # Fingerprinting and Zero Knowledge Proof (ZKP) data
            total_intensity = grayscale_sum(processed_image_path)
            image_intensity_hash = sha256(str(total_intensity).encode()).hexdigest()
            challenge = random.randint(1, 10000)
            challenge_hash = sha256((image_intensity_hash + str(challenge)).encode()).hexdigest()

            # Mining block
            block_data = challenge_hash + sensitivity + str(difficulty)
            new_hash, nonce, mining_time = mine_block(block_data, difficulty, previous_hash)
            total_mining_time += mining_time

            # Create and store the block details
            block = {
                'Block Number': block_number,
                'Sensitivity': sensitivity,
                'Difficulty Level': difficulty,
                'Data': challenge_hash,
                'Nonce': nonce,
                'Previous Hash': previous_hash,
                'New Hash': new_hash
            }

            # Update for next block
            previous_hash = new_hash
            block_number += 1

        # Record total mining time for this sensitivity ratio
        mean_mining_time = total_mining_time / len(images)
        ratio_mining_times.append(mean_mining_time)
        print(f"Mean Mining Time for ratio {ratio}: {mean_mining_time:.4f} seconds")

    return ratio_mining_times

if __name__ == "__main__":
    # Directory containing images
    image_folder = "images"
    processed_folder = "processed_images"

    # Create processed folder if it doesn't exist
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    images = glob.glob(os.path.join(image_folder, "*.jpg"))

    # Process images with each sensitivity ratio
    mining_times = process_images_with_ratios(images)

    # Plotting the results
    ratio_labels = ["0:0:1", "0:1:0", "1:0:0", "0.25:0.25:0.5", "0.25:0.5:0.25", "0.5:0.25:0.25", "0.33:0.33:0.33"]
    plt.figure(figsize=(10, 6))
    plt.bar(ratio_labels, mining_times, color='teal')
    plt.xlabel("Sensitivity Ratio (High:Medium:Low)", fontsize=14)
    plt.ylabel("Mean Mining Time (seconds)", fontsize=14)
    #plt.title("Mean Mining Time for Different Sensitivity Ratios")
    plt.savefig('sensitivity_ratios.png')
    plt.show()
