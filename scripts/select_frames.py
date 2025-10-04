# Quick script to copy diverse frames
import shutil
import os

# Select frames at different intervals
frames_to_annotate = [
    0, 10, 20, 30, 50, 75, 100, 125, 150,  # Early game
    200, 250, 300, 350, 400,                # Mid game
    450, 500, 550, 580                      # Late game
]

# Create selection folder
os.makedirs('data/frames/game1_selected', exist_ok=True)

# Copy selected frames
for i in frames_to_annotate:
    src = f'data/frames/game1/frame_{i:06d}.jpg'
    dst = f'data/frames/game1_selected/frame_{i:06d}.jpg'
    if os.path.exists(src):
        shutil.copy(src, dst)

print(f"Selected {len(frames_to_annotate)} frames for annotation")