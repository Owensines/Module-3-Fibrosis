'''Module 3: count black and white pixels and compute the percentage of white pixels in a .jpg image and extrapolate points'''

from termcolor import colored
import cv2
import numpy as np
import pandas as pd
import time   # <-- ADD THIS

# Start timer
start_time = time.time()

# Load the images you want to analyze
filenames = [
    r"C:\Users\omsin\Desktop\Comp BME\Module-3-Fibrosis\images\MASK_Sk658 Llobe ch010025.jpg",
    r"C:\Users\omsin\Desktop\Comp BME\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010063.jpg",    
    r"C:\Users\omsin\Desktop\Comp BME\Module-3-Fibrosis\images\MASK_Sk658 Llobe ch010065.jpg",
    r"C:\Users\omsin\Desktop\Comp BME\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010115.jpg",
    r"C:\Users\omsin\Desktop\Comp BME\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010158.jpg",
    r"C:\Users\omsin\Desktop\Comp BME\Module-3-Fibrosis\images\MASK_Sk658 Llobe ch010168.jpg",
]

# Depths corresponding to each image
depths = [15, 1000, 3000, 5300, 7000, 9900]

# Lists to store results
white_counts = []
black_counts = []
white_percents = []

print(colored("Counts of pixels by color in each image", "yellow"))

# Process each image one at a time (more memory efficient)
for i, (filename, depth) in enumerate(zip(filenames, depths)):

    img = cv2.imread(filename, 0)

    if img is None:
        print(colored(f"Error loading image: {filename}", "red"))
        continue

    # Convert to binary
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Count pixels
    white = np.count_nonzero(binary == 255)
    total_pixels = binary.size
    black = total_pixels - white

    white_counts.append(white)
    black_counts.append(black)

    # Print counts
    print(colored(f"Image {i}:", "cyan"))
    print(colored(f"White pixels: {white}", "white"))
    print(colored(f"Black pixels: {black}", "grey"))
    print()

    # Compute percentage immediately (avoid second loop)
    white_percent = 100 * white / total_pixels
    white_percents.append(white_percent)

# Print summary
print(colored("Percent white pixels:", "yellow"))

for filename, depth, percent in zip(filenames, depths, white_percents):
    print(colored(f"{filename}:", "red"))
    print(f"{percent:.2f}% White | Depth: {depth} microns")
    print()

'''Write your data to a .csv file'''

df = pd.DataFrame({
    'Filenames': filenames,
    'Depths': depths,
    'White percents': white_percents
})

df.to_csv('Percent_White_Pixels.csv', index=False)

print("The .csv file 'Percent_White_Pixels.csv' has been created.")



#LECTURE 2: UNCOMMENT BELOW
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
# Interpolate a point: given a depth, find the corresponding white pixel percentage
interpolate_depth = float(input(colored(
    "Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))

x = depths
y = white_percents

# Linear interpolation
i_linear = interp1d(x, y, kind='linear')
interpolate_point_linear = i_linear(interpolate_depth)

# Quadratic interpolation
i_quadratic = interp1d(x, y, kind='quadratic')
interpolate_point_quadratic = i_quadratic(interpolate_depth)

print(colored(
    f'Linear interpolation → x: {interpolate_depth}, y: {interpolate_point_linear}', "green"))

print(colored(
    f'Quadratic interpolation → x: {interpolate_depth}, y: {interpolate_point_quadratic}', "green"))

depths_i = depths[:]
depths_i.append(interpolate_depth)

white_percents_i = white_percents[:]
white_percents_i.append(interpolate_point_linear)  # plotting linear by default

# make two plots
fig, axs = plt.subplots(2, 1)

# Original data
axs[0].scatter(depths, white_percents, marker='o', linestyle='-', color='blue')
axs[0].set_title('Plot of depth of image vs percentage white pixels')
axs[0].set_xlabel('depth of image (in microns)')
axs[0].set_ylabel('white pixels as a percentage of total pixels')
axs[0].grid(True)

# With interpolated point
axs[1].scatter(depths_i, white_percents_i, marker='o',
               linestyle='-', color='blue')
axs[1].set_title(
    'Plot of depth of image vs percentage white pixels with interpolated point (in red)')
axs[1].set_xlabel('depth of image (in microns)')
axs[1].set_ylabel('white pixels as a percentage of total pixels')
axs[1].grid(True)

axs[1].scatter(depths_i[-1], white_percents_i[-1],
               color='red', s=100, label='Linear interpolated point')
# Highlight quadratic interpolated point in green
axs[1].scatter(interpolate_depth, interpolate_point_quadratic, color='green', s=100, label='Quadratic interpolated point')
axs[1].legend()

plt.tight_layout()
plt.show()