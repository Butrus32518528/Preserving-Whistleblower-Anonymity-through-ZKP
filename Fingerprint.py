from PIL import Image

def grayscale_sum(image_path):
    # Open the image
    image = Image.open(image_path)

    # Convert the image to grayscale
    grayscale_image = image.convert("L")

    # Get pixel values as a flattened list
    pixel_values = list(grayscale_image.getdata())

    # Sum the intensity values
    total_intensity = sum(pixel_values)

    # Return the sum of intensities
    return total_intensity

