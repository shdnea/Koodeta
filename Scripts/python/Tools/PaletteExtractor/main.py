from PIL import Image
import numpy as np
from collections import Counter

def extract_colors(image_path, num_colors=5):
    # Open the image and convert it to RGB
    image = Image.open(image_path).convert('RGB')

    # Resize to speed up processing (optional)
    image = image.resize((image.width // 5, image.height // 5))

    # Convert to numpy array
    image_array = np.array(image)

    # Reshape the array to a list of pixels
    pixels = image_array.reshape(-1, 3)

    # Count the most common colors
    pixel_counts = Counter(map(tuple, pixels))
    
    # Get the most common colors
    common_colors = pixel_counts.most_common(num_colors)
    
    # Convert them to hex values
    hex_colors = [f'#{r:02x}{g:02x}{b:02x}' for (r, g, b), _ in common_colors]
    
    return hex_colors